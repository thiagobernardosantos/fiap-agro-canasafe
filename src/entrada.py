"""Leitura e validação de dados digitados pelo usuário."""
import re


def ler_texto(msg, tam_max=50):
    while True:
        valor = input(msg).strip()
        if valor and len(valor) <= tam_max:
            return valor
        print(f"  [!] Informe um texto não vazio com até {tam_max} caracteres.")


def ler_float(msg, minimo, maximo):
    while True:
        bruto = input(msg).strip().replace(",", ".")
        try:
            valor = float(bruto)
        except ValueError:
            print("  [!] Digite apenas números (ex.: 12,5).")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"  [!] O valor deve estar entre {minimo} e {maximo}.")


def ler_int(msg, minimo, maximo):
    while True:
        bruto = input(msg).strip()
        if bruto.isdigit() and minimo <= int(bruto) <= maximo:
            return int(bruto)
        print(f"  [!] Digite um número inteiro entre {minimo} e {maximo}.")


def ler_opcao(msg, opcoes):
    """Aceita apenas valores presentes na tupla/lista 'opcoes' (case-insensitive)."""
    while True:
        valor = input(msg).strip().upper().replace("Â", "A").replace("Ç", "C")
        if valor in opcoes:
            return valor
        print(f"  [!] Opções válidas: {', '.join(opcoes)}.")


def ler_safra(msg):
    """Formato AAAA/AA, ex.: 2025/26."""
    while True:
        valor = input(msg).strip()
        if re.fullmatch(r"\d{4}/\d{2}", valor):
            return valor
        print("  [!] Use o formato AAAA/AA (ex.: 2025/26).")
