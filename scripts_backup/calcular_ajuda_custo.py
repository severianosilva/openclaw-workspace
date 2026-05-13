#!/usr/bin/env python3
"""Calculadora de Ajuda de Custo - TJMG"""

def calcular():
    valor_dia = float(input("Valor da ajuda (R$/dia): ") or "100")
    anos = range(2021, 2026)
    total = 0
    for ano in anos:
        dias = int(input(f"Dias de afastamento em {ano}: ") or "0")
        subtotal = dias * valor_dia
        total += subtotal
        print(f"  {ano}: {dias} dias = R$ {subtotal:,.2f}")
    print(f"\nTOTAL 5 ANOS: R$ {total:,.2f}")

if __name__ == "__main__":
    calcular()
