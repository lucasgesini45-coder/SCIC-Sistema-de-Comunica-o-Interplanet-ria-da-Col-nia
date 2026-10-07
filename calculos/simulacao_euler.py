"""
Simulação da latência de um módulo ao longo do tempo com o MÉTODO DE EULER.

Situação: depois de um pico de latência, o enlace vai se "acalmando" e a latência
volta ao seu valor normal. Isso pode ser descrito por uma equação simples:

        dL/dt = -a * (L - L_normal)

  L        = latência no instante t
  L_normal = latência normal do módulo (aqui: a média observada no CSV)
  a        = rapidez da recuperação (quanto maior, mais rápido volta ao normal)

O método de Euler resolve isso em pequenos passos de tamanho h:
        L_novo = L_atual + h * (-a * (L_atual - L_normal))

Como essa equação também tem solução exata, L(t) = L_normal + (L0 - L_normal) * e^(-a*t),
dá para medir o ERRO do Euler (absoluto e relativo) e ver como o passo h influencia.
"""

import math

from modulos.inserir_dados import carregar_csv, escolher_opcao, ler_float

TEMPO_TOTAL = 10.0  # ciclos simulados
RAPIDEZ = 0.5  # o "a" da equação: recuperação moderada


def euler(latencia_inicial, latencia_normal, rapidez, passo, tempo_total):
    """Aplica o método de Euler e devolve a lista de pontos (tempo, latência)."""
    pontos = [(0.0, latencia_inicial)]
    tempo, latencia = 0.0, latencia_inicial
    quantidade_de_passos = round(tempo_total / passo)
    for _ in range(quantidade_de_passos):
        # inclinação da curva neste ponto (quanto a latência está "descendo")
        derivada = -rapidez * (latencia - latencia_normal)
        latencia = latencia + passo * derivada  # um pequeno passo na direção da inclinação
        tempo += passo
        pontos.append((tempo, latencia))
    return pontos


def solucao_exata(latencia_inicial, latencia_normal, rapidez, tempo):
    """Valor exato da equação em um instante t (serve de referência para medir o erro)."""
    return latencia_normal + (latencia_inicial - latencia_normal) * math.exp(-rapidez * tempo)


def simular_recuperacao():
    dados = carregar_csv()
    if dados is None:
        return

    # O usuário escolhe um módulo; usamos a média e o pico dele como ponto de partida
    nomes = sorted(dados["nome"].unique())
    nome = escolher_opcao("\nQual módulo simular?", nomes)
    registros = dados[dados["nome"] == nome]
    latencia_normal = registros["latencia_observada"].mean()
    latencia_inicial = registros["latencia_observada"].max()  # o pior pico registrado

    print(f"\n--- Recuperação da latência após um pico: {nome} ---")
    print(f"Latência normal (média): {latencia_normal:.1f} ms | Pico inicial: {latencia_inicial:.1f} ms")
    print(f"Equação: dL/dt = -{RAPIDEZ} * (L - {latencia_normal:.1f})  |  tempo simulado: {TEMPO_TOTAL:.0f} ciclos")

    passo = ler_float("Tamanho do passo h (ex: 1, 0.5, 0.1): ", minimo=0.01)
    if passo > TEMPO_TOTAL:
        print("O passo não pode ser maior que o tempo total.")
        return

    pontos = euler(latencia_inicial, latencia_normal, RAPIDEZ, passo, TEMPO_TOTAL)

    # Mostra alguns pontos (no máximo 11) comparando Euler x exato
    print(f"\n{'Tempo':>7}{'Euler (ms)':>14}{'Exato (ms)':>14}{'Erro abs':>12}{'Erro rel':>11}")
    pulo = max(1, len(pontos) // 10)
    for tempo, valor_euler in pontos[::pulo]:
        exato = solucao_exata(latencia_inicial, latencia_normal, RAPIDEZ, tempo)
        erro_absoluto = abs(valor_euler - exato)
        erro_relativo = erro_absoluto / exato * 100
        print(f"{tempo:>7.1f}{valor_euler:>14.2f}{exato:>14.2f}{erro_absoluto:>12.3f}{erro_relativo:>10.3f}%")

    # Compara vários tamanhos de passo: passo menor -> erro menor (mas mais contas)
    print("\nEfeito do tamanho do passo no erro final (t = 10):")
    print(f"{'Passo h':>9}{'Nº de passos':>14}{'Erro absoluto (ms)':>21}")
    exato_final = solucao_exata(latencia_inicial, latencia_normal, RAPIDEZ, TEMPO_TOTAL)
    for h in (2.0, 1.0, 0.5, 0.1, 0.01):
        valor_final = euler(latencia_inicial, latencia_normal, RAPIDEZ, h, TEMPO_TOTAL)[-1][1]
        print(f"{h:>9}{round(TEMPO_TOTAL / h):>14}{abs(valor_final - exato_final):>21.5f}")

    print("\nInterpretação: o Euler é uma aproximação. Quanto menor o passo, mais perto do valor exato,")
    print("porque o erro de cada passo é menor. Num sistema real, escolhe-se um passo que equilibre")
    print("precisão e tempo de cálculo. Aqui, ele mostra em quantos ciclos o enlace volta ao normal.")
