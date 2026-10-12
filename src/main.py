"""CanaSafe - Monitor de perdas na colheita de cana-de-açúcar (Agronegócio)."""
import oracledb
import regras
import entrada
import arquivos
import db


# ---------- PROCEDIMENTOS (não retornam valor) ----------
def exibir_menu():
    print("\n" + "=" * 50)
    print("   CANASAFE - Perdas na colheita de cana")
    print("=" * 50)
    print(" 1 - Registrar colheita")
    print(" 2 - Listar colheitas")
    print(" 3 - Atualizar perda de um registro")
    print(" 4 - Remover registro")
    print(" 5 - Relatório (tela + TXT)")
    print(" 6 - Exportar dados para JSON")
    print(" 7 - Ler JSON exportado")
    print(" 0 - Sair")


def exibir_tabela(registros):
    """Monta uma 'tabela de memória' (lista de listas) e imprime formatada."""
    if not registros:
        print("  Nenhum registro encontrado.")
        return
    cabecalho = ["ID", "Talhão", "Safra", "Tipo", "Prod(t)", "Perda %", "Perda t", "Perda R$", "Status"]
    tabela = [cabecalho]
    for r in registros:
        total = r["area_ha"] * r["produtividade"]
        tabela.append([r["id"], r["talhao"], r["safra"], r["tipo"], f"{total:.1f}",
                       f"{r['perda_pct']:.1f}", f"{r['perda_ton']:.1f}",
                       f"{r['perda_rs']:,.2f}", r["status"]])
    larguras = [max(len(str(l[i])) for l in tabela) for i in range(len(cabecalho))]
    for n, linha in enumerate(tabela):
        print(" | ".join(str(c).ljust(larguras[i]) for i, c in enumerate(linha)))
        if n == 0:
            print("-+-".join("-" * w for w in larguras))


def exibir_recomendacoes(tipo, status):
    print(f"\n  Status: {status}")
    for dica in regras.recomendar(tipo, status):
        print(f"   - {dica}")


# ---------- FUNÇÕES (retornam valor) ----------
def montar_registro(talhao, safra, area, produt, tipo, perda_pct):
    producao, perda_t, perda_rs = regras.calcular_perda(area, produt, perda_pct)
    return {"talhao": talhao, "safra": safra, "area_ha": area, "produtividade": produt,
            "tipo": tipo, "perda_pct": perda_pct, "perda_ton": perda_t,
            "perda_rs": perda_rs, "status": regras.classificar(tipo, perda_pct)}


def calcular_resumo(registros):
    """Retorna dicionário com totais e a contagem por status."""
    por_status = {}
    for r in registros:
        por_status[r["status"]] = por_status.get(r["status"], 0) + 1
    return {"Total de registros": len(registros),
            "Perda total (t)": round(sum(r["perda_ton"] for r in registros), 2),
            "Prejuízo estimado (R$)": f"{sum(r['perda_rs'] for r in registros):,.2f}",
            "Registros por status": por_status}


# ---------- AÇÕES DO MENU ----------
def registrar(conn):
    print("\n--- Nova colheita ---")
    talhao = entrada.ler_texto("Nome/código do talhão: ")
    safra = entrada.ler_safra("Safra (AAAA/AA): ")
    area = entrada.ler_float("Área colhida (ha): ", 0.1, 100000)
    produt = entrada.ler_float("Produtividade (t/ha): ", 1, 300)
    tipo = entrada.ler_opcao("Tipo de colheita [MANUAL/MECANICA]: ", regras.TIPOS_COLHEITA)
    perda = entrada.ler_float("Perda medida na colheita (%): ", 0, 100)
    reg = montar_registro(talhao, safra, area, produt, tipo, perda)
    db.inserir(conn, reg)
    print(f"\n  Registrado! Perda de {reg['perda_ton']:.1f} t "
          f"(≈ R$ {reg['perda_rs']:,.2f}).")
    exibir_recomendacoes(tipo, reg["status"])


def atualizar_perda(conn):
    registros = db.listar(conn)
    exibir_tabela(registros)
    if not registros:
        return
    ids = [r["id"] for r in registros]
    id_reg = entrada.ler_int("ID do registro: ", 1, max(ids))
    alvo = next((r for r in registros if r["id"] == id_reg), None)
    if alvo is None:
        print("  [!] ID não encontrado.")
        return
    nova = entrada.ler_float("Nova perda (%): ", 0, 100)
    novo = montar_registro(alvo["talhao"], alvo["safra"], alvo["area_ha"],
                           alvo["produtividade"], alvo["tipo"], nova)
    db.atualizar(conn, id_reg, nova, novo["perda_ton"], novo["perda_rs"], novo["status"])
    print("  Registro atualizado.")
    exibir_recomendacoes(alvo["tipo"], novo["status"])


def remover_registro(conn):
    registros = db.listar(conn)
    exibir_tabela(registros)
    if not registros:
        return
    id_reg = entrada.ler_int("ID a remover: ", 1, max(r["id"] for r in registros))
    if entrada.ler_opcao("Confirma a exclusão? [S/N]: ", ("S", "N")) == "S":
        print("  Removido." if db.remover(conn, id_reg) else "  [!] ID não encontrado.")


def relatorio(conn):
    registros = db.listar(conn)
    exibir_tabela(registros)
    if not registros:
        return
    resumo = calcular_resumo(registros)
    print()
    for k, v in resumo.items():
        print(f"{k}: {v}")
    print("Arquivo gerado:", arquivos.gerar_relatorio_txt(registros, resumo))


def main():
    try:
        conn = db.conectar()
        db.criar_tabela(conn)
    except oracledb.Error as e:
        print(f"Não foi possível conectar ao Oracle: {e}")
        return
    acoes = {1: registrar, 2: lambda c: exibir_tabela(db.listar(c)),
             3: atualizar_perda, 4: remover_registro, 5: relatorio,
             6: lambda c: print("  Exportado em:", arquivos.exportar_json(db.listar(c))),
             7: lambda c: exibir_tabela(arquivos.importar_json())}
    while True:
        exibir_menu()
        op = entrada.ler_int("Escolha: ", 0, 7)
        if op == 0:
            break
        try:
            acoes[op](conn)
        except oracledb.Error as e:
            print(f"  [!] Erro no banco de dados: {e}")
    conn.close()
    print("Até a próxima safra!")


if __name__ == "__main__":
    main()
