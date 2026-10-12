"""Manipulação de arquivos: JSON (exportar/importar) e TXT (relatório)."""
import json
from datetime import datetime


def exportar_json(registros, caminho="dados_colheita.json"):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=4, default=str)
    return caminho


def importar_json(caminho="dados_colheita.json"):
    """Lê o JSON; retorna lista vazia se não existir ou estiver inválido."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  [!] Arquivo '{caminho}' não encontrado.")
    except json.JSONDecodeError:
        print(f"  [!] Arquivo '{caminho}' não é um JSON válido.")
    return []


def gerar_relatorio_txt(registros, resumo, caminho="relatorio_perdas.txt"):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR\n")
        f.write(f"Gerado em {datetime.now():%d/%m/%Y %H:%M}\n")
        f.write("=" * 60 + "\n")
        for r in registros:
            f.write(f"Talhão {r['talhao']} | Safra {r['safra']} | {r['tipo']} | "
                    f"perda {r['perda_pct']:.1f}% ({r['perda_ton']:.1f} t, "
                    f"R$ {r['perda_rs']:,.2f}) | {r['status']}\n")
        f.write("=" * 60 + "\n")
        for chave, valor in resumo.items():
            f.write(f"{chave}: {valor}\n")
    return caminho
