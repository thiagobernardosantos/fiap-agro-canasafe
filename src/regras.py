"""Regras de negócio: cálculo e classificação de perdas na colheita de cana."""

# Tupla: tipos de colheita válidos (imutável)
TIPOS_COLHEITA = ("MANUAL", "MECANICA")

# Dicionário: limite de perda aceitável (%) por tipo, segundo os estudos citados no enunciado
LIMITE_PERDA = {"MANUAL": 5.0, "MECANICA": 15.0}

PRECO_TON_PADRAO = 150.0  # R$ por tonelada de cana (valor de referência editável)


def calcular_perda(area_ha, produtividade, perda_pct, preco_ton=PRECO_TON_PADRAO):
    """Retorna (producao_total_t, perda_t, perda_rs)."""
    producao_total = area_ha * produtividade
    perda_t = producao_total * perda_pct / 100
    return round(producao_total, 2), round(perda_t, 2), round(perda_t * preco_ton, 2)


def classificar(tipo, perda_pct):
    """Classifica a perda em ADEQUADA, ATENCAO ou CRITICA."""
    limite = LIMITE_PERDA[tipo]
    if perda_pct <= limite:
        return "ADEQUADA"
    if perda_pct <= limite * 1.5:
        return "ATENCAO"
    return "CRITICA"


def recomendar(tipo, status):
    """Retorna lista de recomendações conforme o tipo de colheita e o status."""
    if status == "ADEQUADA":
        return ["Perda dentro do esperado. Mantenha o monitoramento a cada safra."]
    dicas = ["Revise o planejamento do plantio à colheita (espaçamento e alinhamento).",
             "Defina o momento ideal de colheita (maturação e umidade da cana)."]
    if tipo == "MECANICA":
        dicas += ["Calibre a colhedora (velocidade, altura de corte, rotação dos extratores).",
                  "Treine os operadores e avalie o piloto automático/geolocalização."]
    else:
        dicas += ["Treine a equipe de corte para reduzir o toco alto e pontas desperdiçadas."]
    if status == "CRITICA":
        dicas.append("PRIORIDADE: faça uma auditoria de campo no talhão antes da próxima safra.")
    return dicas
