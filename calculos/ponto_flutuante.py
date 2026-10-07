"""Precisão numérica: ponto flutuante, arredondamento e erro aceitável (menu: Análises > opção 4)."""

import math

import numpy as np

from modulos.inserir_dados import LIMITE_ALERTA, LIMITE_ATENCAO, carregar_csv


def precisao_numerica():
    """Mostra, com exemplos, por que números decimais no computador são aproximações."""
    print("\n====== PRECISÃO NUMÉRICA E PONTO FLUTUANTE ======")

    # --- Parte 1 ---
    # O computador guarda decimais em binário, então muitos valores são aproximados
    print("\n1) Por que 0,1 + 0,2 não é exatamente 0,3 no computador?")
    soma = 0.1 + 0.2  # deveria dar 0.3, mas não dá exatamente
    print(f"   0.1 + 0.2 = {soma!r}")
    print(f"   0.1 + 0.2 == 0.3 ?  {soma == 0.3}")
    print(f"   Erro absoluto da soma: {abs(soma - 0.3):.2e}")
    print(f"   Comparação segura (math.isclose): {math.isclose(soma, 0.3)}")
    print("   Motivo: 0,1 é uma dízima em binário e é guardado de forma aproximada.")

    # --- Parte 2 ---
    # Erro acumulado ao somar muitas vezes (ex.: somar leituras de latência)
    print("\n2) Erro acumulado em somas repetidas")
    # Somamos com um laço (e não com sum()) porque o Python novo compensa o erro dentro do sum()
    soma_mil_vezes = 0.0
    for _ in range(1000):
        soma_mil_vezes += 0.1  # cada soma carrega um errinho que vai se acumulando
    print(f"   Somar 0.1 mil vezes = {soma_mil_vezes!r} (esperado 100.0)")
    print(f"   Erro absoluto: {abs(soma_mil_vezes - 100):.2e} | erro relativo: {abs(soma_mil_vezes - 100) / 100 * 100:.2e}%")

    # --- Parte 3 ---
    # Precisão simples (float32) x dupla (float64)
    print("\n3) Precisão simples (float32) x dupla (float64) para 0,1")
    print(f"   float64: {np.float64(0.1):.20f}")
    print(f"   float32: {float(np.float32(0.1)):.20f}")

    # --- Parte 4 ---
    # Efeito do arredondamento nos dados da colônia
    dados = carregar_csv()
    if dados is not None:
        print("\n4) Arredondamento nos dados da colônia")
        r = dados.iloc[0]  # pega só o primeiro registro como exemplo
        ea_exato = float(abs(r["latencia_observada"] - r["latencia_prevista"]))
        er_exato = float(ea_exato / r["latencia_prevista"] * 100)
        print(f"   {r['nome']} (ciclo {int(r['ciclo'])}): observada {r['latencia_observada']} ms, prevista {r['latencia_prevista']} ms")
        print(f"   Erro absoluto = {ea_exato!r} ms | erro relativo sem arredondar = {er_exato!r}%")
        print(f"   Erro relativo arredondado em 2 casas (como no CSV) = {round(er_exato, 2)}%")
        print(f"   Diferença causada pelo arredondamento: {abs(er_exato - round(er_exato, 2)):.2e} ponto percentual")
        print("   Essa diferença é minúscula perto dos limites de decisão abaixo, então não muda o status.")

    # --- Parte 5 ---
    # Quando um erro é aceitável ou preocupante
    print("\n5) Quando o erro é aceitável ou preocupante na colônia?")
    print(f"   Até {LIMITE_ATENCAO:.0f}%  -> aceitável (Ativo).")
    print(f"   {LIMITE_ATENCAO:.0f}% a {LIMITE_ALERTA:.0f}% -> preocupante, acompanhar (Atenção).")
    print(f"   Acima de {LIMITE_ALERTA:.0f}% -> crítico, exige ação (Alerta).")
    print("   Erros de ponto flutuante (~1e-16) são desprezíveis; o que importa é o desvio real do enlace.")
    print("   Usa-se erro relativo porque 20 ms pesam muito em 100 ms e pouco em 5000 ms.")
    print("\n=================================================")
