"""
Modelo simples de previsão da latência (regressão linear) e avaliação de desempenho.

Os dados são divididos em três partes:
    TREINO     (60%) -> o modelo aprende aqui;
    VALIDAÇÃO  (20%) -> usada para ESCOLHER o melhor modelo (Grid/Random Search);
    TESTE      (20%) -> guardado até o fim, só para a nota final, sem "viciar" a escolha.

O modelo relaciona:  tipo do módulo + potência + ciclo  ->  latência observada.
"""

import numpy as np

from modulos.inserir_dados import (
    carregar_csv,
    escolher_opcao,
    ler_float,
    ler_inteiro,
)

SEMENTE = 42  # semente fixa: o sorteio treino/teste é sempre o mesmo
PROPORCAO_TESTE = 0.2  # 20% dos registros ficam para o teste
PROPORCAO_VALIDACAO = 0.2  # 20% ficam para a validação
VALORES_DE_LAMBDA = [0, 0.1, 1, 10, 100, 1000]  # forças de regularização testadas
MINIMO_REGISTROS = 12  # abaixo disso não vale a pena dividir os dados


# ------------------------------------------------------------
# Métricas de avaliação
# ------------------------------------------------------------
def calcular_metricas(valores_reais, valores_previstos):
    """Devolve MAE, MSE, RMSE e R² comparando o que aconteceu com o que foi previsto."""
    reais = np.asarray(valores_reais, float)
    previstos = np.asarray(valores_previstos, float)
    erros = reais - previstos

    mae = np.mean(np.abs(erros))  # erro absoluto médio (em ms)
    mse = np.mean(erros**2)  # erro quadrático médio (castiga erros grandes)
    rmse = np.sqrt(mse)  # raiz do MSE: volta para a unidade original (ms)

    # R²: quanto da variação da latência o modelo consegue explicar (1 = tudo)
    soma_total = np.sum((reais - reais.mean()) ** 2)
    if len(reais) > 1 and soma_total > 0:
        r2 = 1 - np.sum(erros**2) / soma_total
    else:
        r2 = float("nan")  # não dá para calcular com 1 registro ou sem variação
    return float(mae), float(mse), float(rmse), float(r2)


def aic_bic(valores_reais, valores_previstos, parametros):
    """
    AIC e BIC servem para comparar modelos: menor é melhor.
    Os dois premiam quem erra pouco e punem modelos com parâmetros demais
    (o BIC pune mais).
    """
    n = len(valores_reais)
    soma_dos_quadrados = np.sum((np.asarray(valores_reais) - np.asarray(valores_previstos)) ** 2)
    soma_dos_quadrados = max(soma_dos_quadrados, 1e-12)  # evita log(0)
    aic = n * np.log(soma_dos_quadrados / n) + 2 * parametros
    bic = n * np.log(soma_dos_quadrados / n) + parametros * np.log(n)
    return aic, bic


# ------------------------------------------------------------
# Treino e previsão
# ------------------------------------------------------------
def montar_X(dados, tipos_usados, usar_ciclo):
    """Monta a tabela de entradas do modelo: uma coluna 0/1 por tipo, a potência e (opcional) o ciclo."""
    colunas = [(dados["tipo"] == tipo).astype(float).to_numpy() for tipo in tipos_usados]
    colunas.append(dados["potencia"].to_numpy(float))
    if usar_ciclo:
        colunas.append(dados["ciclo"].to_numpy(float))
    return np.column_stack(colunas)


def dividir(dados):
    """Embaralha os registros e separa em treino (60%), validação (20%) e teste (20%)."""
    gerador = np.random.default_rng(SEMENTE)
    ordem_embaralhada = gerador.permutation(len(dados))
    quantidade_teste = max(1, int(len(dados) * PROPORCAO_TESTE))
    quantidade_validacao = max(1, int(len(dados) * PROPORCAO_VALIDACAO))
    teste = dados.iloc[ordem_embaralhada[:quantidade_teste]]
    validacao = dados.iloc[ordem_embaralhada[quantidade_teste : quantidade_teste + quantidade_validacao]]
    treino = dados.iloc[ordem_embaralhada[quantidade_teste + quantidade_validacao :]]
    return treino, validacao, teste


def treinar(treino, usar_ciclo=True, lambda_ridge=0.0):
    """
    Ajusta a regressão linear pelo método dos mínimos quadrados e devolve o modelo.
    lambda_ridge > 0 ativa a regularização: "puxa" os coeficientes para perto de zero,
    o que evita que o modelo se agarre demais aos dados de treino. Com 0, é a regressão comum.
    """
    tipos_usados = sorted(treino["tipo"].unique())
    X = montar_X(treino, tipos_usados, usar_ciclo)
    y = treino["latencia_observada"].to_numpy(float)
    # Equação normal com regularização: (X'X + lambda * I) w = X'y
    identidade = np.eye(X.shape[1])
    coeficientes = np.linalg.solve(X.T @ X + lambda_ridge * identidade, X.T @ y)
    return {
        "coef": coeficientes,
        "tipos": tipos_usados,
        "usar_ciclo": usar_ciclo,
        "lambda": lambda_ridge,
        "k": int(np.linalg.matrix_rank(X)),  # nº de parâmetros reais (usado no AIC/BIC)
    }


def prever(modelo, dados):
    """Aplica o modelo treinado em novos dados e devolve as latências previstas."""
    return montar_X(dados, modelo["tipos"], modelo["usar_ciclo"]) @ modelo["coef"]


def preparar():
    """Carrega o CSV, divide em treino/validação/teste e treina. Devolve tudo pronto (ou None)."""
    dados = carregar_csv(MINIMO_REGISTROS)
    if dados is None:
        return None
    treino, validacao, teste = dividir(dados)
    return dados, treino, validacao, teste, treinar(treino, True)


def rmse_na_validacao(modelo, validacao):
    """Nota usada para comparar candidatos: RMSE (em ms) nos dados de validação."""
    reais = validacao["latencia_observada"].to_numpy(float)
    return calcular_metricas(reais, prever(modelo, validacao))[2]


# ------------------------------------------------------------
# Telas do menu
# ------------------------------------------------------------
def executar_previsao():
    pronto = preparar()
    if pronto is None:
        return
    dados, treino, validacao, teste, modelo = pronto

    print("\n--- Modelo de previsão da latência ---")
    print(
        f"{len(dados)} registros: {len(treino)} para treino, {len(validacao)} para validação "
        f"e {len(teste)} para teste (semente {SEMENTE})."
    )
    print("Modelo: regressão linear (tipo do módulo + potência + ciclo).")

    # Mostra o que o modelo "aprendeu" em linguagem simples
    coeficientes = modelo["coef"]
    n_tipos = len(modelo["tipos"])
    print("\nO que o modelo aprendeu:")
    for tipo, coeficiente in zip(modelo["tipos"], coeficientes[:n_tipos]):
        print(f"  Latência base de {tipo}: {coeficiente:.1f} ms")
    print(f"  Efeito da potência: {coeficientes[n_tipos]:+.3f} ms por W")
    print(f"  Efeito do ciclo:    {coeficientes[n_tipos + 1]:+.3f} ms por ciclo")

    # Previsões nos registros de teste, comparadas com o que realmente aconteceu
    previstas = prever(modelo, teste)
    print("\nPrevisões nos registros de teste (que o modelo não viu no treino):")
    print(f"{'Ciclo':<6}{'Código':<9}{'Observada':<11}{'Prevista':<10}{'Erro abs':<10}Erro rel")
    print("-" * 56)
    for (_, linha), prevista in list(zip(teste.iterrows(), previstas))[:10]:
        erro_absoluto = abs(linha["latencia_observada"] - prevista)
        erro_relativo = erro_absoluto / abs(prevista) * 100 if prevista else 0
        print(
            f"{int(linha['ciclo']):<6}{linha['codigo_sensor']:<9}{linha['latencia_observada']:<11.1f}"
            f"{prevista:<10.1f}{erro_absoluto:<10.1f}{erro_relativo:.1f}%"
        )
    if len(teste) > 10:
        print(f"(mostrando 10 de {len(teste)})")

    # Previsão para um cenário digitado pelo usuário
    if input("\nPrever a latência de um novo cenário? (s/n): ").strip().lower() == "s":
        tipo = escolher_opcao("\nTipo do módulo:", modelo["tipos"])
        potencia = ler_float("Potência (W): ")
        ciclo = ler_inteiro("Ciclo: ", 1, 10**6)
        # Mesmo formato das entradas do treino: um 1 no tipo escolhido, depois potência e ciclo
        entrada = [1.0 if t == tipo else 0.0 for t in modelo["tipos"]] + [potencia, float(ciclo)]
        print(f"\nLatência prevista: {float(np.array(entrada) @ coeficientes):.1f} ms")


def avaliar_desempenho():
    pronto = preparar()
    if pronto is None:
        return
    dados, treino, validacao, teste, modelo = pronto

    reais_teste = teste["latencia_observada"].to_numpy(float)
    mae, mse, rmse, r2 = calcular_metricas(reais_teste, prever(modelo, teste))
    # Referência (baseline): a latência prevista que já veio gravada no CSV
    referencia = calcular_metricas(reais_teste, teste["latencia_prevista"].to_numpy(float))

    print("\n--- Avaliação de desempenho (conjunto de teste) ---")
    print(f"Treino: {len(treino)} | Validação: {len(validacao)} | Teste: {len(teste)} registros\n")

    # Ingênuo: prever sempre a média do treino. Se o modelo não vencer isso, não vale nada.
    ingenuo = calcular_metricas(reais_teste, np.full(len(reais_teste), treino["latencia_observada"].mean()))
    print(f"{'Métrica':<8}{'Modelo':>12}{'Prevista do CSV':>18}{'Só a média':>14}")
    for nome, valor_modelo, valor_referencia, valor_ingenuo in zip(
        ["MAE", "MSE", "RMSE", "R²"], (mae, mse, rmse, r2), referencia, ingenuo
    ):
        print(f"{nome:<8}{valor_modelo:>12.3f}{valor_referencia:>18.3f}{valor_ingenuo:>14.3f}")
    print("(Prevista do CSV = latência prevista já gravada na base. Só a média = previsão ingênua, a mais simples possível.)")

    # Interpretação: um número sozinho não conta a história toda
    print("\nInterpretação:")
    if r2 == r2:  # r2 == r2 é falso só quando r2 é NaN
        nivel = "alto" if r2 >= 0.9 else "moderado" if r2 >= 0.7 else "baixo"
        print(f"- R² {nivel} ({r2:.3f}): o modelo explica {r2 * 100:.1f}% da variação da latência.")
        if r2 >= 0.9:
            print("  Mas R² alto não significa modelo perfeito: ele não mostra o tamanho dos erros em ms.")
        else:
            print("  Sobra variação que o modelo não explica (ex: anomalias pontuais de latência).")
    if mae > 0:
        razao = rmse / mae
        if razao > 1.3:
            print(f"- RMSE ({rmse:.1f}) bem maior que MAE ({mae:.1f}): há alguns registros com erro grande.")
        else:
            print(f"- RMSE ({rmse:.1f}) próximo do MAE ({mae:.1f}): erros distribuídos de forma parecida.")
    print(f"- Em média o modelo erra {mae:.1f} ms. Para saber se isso é aceitável, compare com o")
    print("  limite de erro relativo da colônia, e use sempre mais de uma métrica.")
    print("- Cuidado: os dados são simulados e a latência prevista nasce de uma fórmula parecida com a")
    print("  que o modelo aprende. Com dados reais da colônia, o resultado poderia ser bem diferente.")

    # Comparação de dois modelos com AIC e BIC (no treino)
    reais_treino = treino["latencia_observada"].to_numpy(float)
    modelo_sem_ciclo = treinar(treino, usar_ciclo=False)
    print("\nComparação de modelos (AIC e BIC no treino; menor é melhor):")
    print(f"{'Modelo':<34}{'AIC':>10}{'BIC':>10}")
    resultados = {}
    for nome, candidato in [("A: tipo + potência", modelo_sem_ciclo), ("B: tipo + potência + ciclo", modelo)]:
        aic, bic = aic_bic(reais_treino, prever(candidato, treino), candidato["k"])
        resultados[nome[0]] = (aic, bic)  # a chave é a letra: "A" ou "B"
        print(f"{nome:<34}{aic:>10.1f}{bic:>10.1f}")
    melhor_aic = min(resultados, key=lambda letra: resultados[letra][0])
    melhor_bic = min(resultados, key=lambda letra: resultados[letra][1])
    print(f"Menor AIC: modelo {melhor_aic} | Menor BIC: modelo {melhor_bic} (o BIC penaliza mais a complexidade).")


def busca_de_hiperparametros():
    """
    Grid Search e Random Search: duas maneiras de ESCOLHER o melhor modelo.
      - Grid Search: testa TODAS as combinações de uma grade.
      - Random Search: sorteia algumas combinações (mais barato quando a grade é enorme).
    A escolha é feita pelo RMSE na VALIDAÇÃO; o TESTE só é usado no final, uma única vez.
    """
    pronto = preparar()
    if pronto is None:
        return
    dados, treino, validacao, teste, _ = pronto

    print("\n--- Escolha do melhor modelo (Grid Search e Random Search) ---")
    print(f"Treino: {len(treino)} | Validação: {len(validacao)} | Teste: {len(teste)} registros")
    print("Parâmetros testados: usar o ciclo (sim/não) e a força de regularização lambda.\n")

    # A grade: todas as combinações possíveis
    grade = [(usar_ciclo, lamb) for usar_ciclo in (True, False) for lamb in VALORES_DE_LAMBDA]

    # --- Grid Search: testa tudo ---
    print(f"GRID SEARCH ({len(grade)} combinações):")
    print(f"  {'Usa ciclo':<11}{'Lambda':>8}{'RMSE validação':>17}")
    melhor_grid = None
    for usar_ciclo, lamb in grade:
        candidato = treinar(treino, usar_ciclo, lamb)
        rmse_val = rmse_na_validacao(candidato, validacao)
        print(f"  {'sim' if usar_ciclo else 'não':<11}{lamb:>8}{rmse_val:>17.3f}")
        if melhor_grid is None or rmse_val < melhor_grid[0]:
            melhor_grid = (rmse_val, usar_ciclo, lamb)
    print(f"  Melhor da grade: ciclo={'sim' if melhor_grid[1] else 'não'}, lambda={melhor_grid[2]} (RMSE {melhor_grid[0]:.3f})")

    # --- Random Search: sorteia só 5 combinações da grade ---
    sorteador = np.random.default_rng(SEMENTE)
    escolhidas = sorteador.choice(len(grade), size=5, replace=False)
    print("\nRANDOM SEARCH (5 combinações sorteadas):")
    melhor_random = None
    for indice in escolhidas:
        usar_ciclo, lamb = grade[indice]
        rmse_val = rmse_na_validacao(treinar(treino, usar_ciclo, lamb), validacao)
        print(f"  ciclo={'sim' if usar_ciclo else 'não':<4} lambda={lamb:<7} RMSE validação {rmse_val:.3f}")
        if melhor_random is None or rmse_val < melhor_random[0]:
            melhor_random = (rmse_val, usar_ciclo, lamb)
    print(f"  Melhor do sorteio: ciclo={'sim' if melhor_random[1] else 'não'}, lambda={melhor_random[2]} (RMSE {melhor_random[0]:.3f})")

    # --- Nota final: o campeão da grade é avaliado UMA vez no teste ---
    campeao = treinar(treino, melhor_grid[1], melhor_grid[2])
    reais_teste = teste["latencia_observada"].to_numpy(float)
    mae, mse, rmse, r2 = calcular_metricas(reais_teste, prever(campeao, teste))
    print("\nMODELO ESCOLHIDO avaliado no TESTE (dados que não influenciaram a escolha):")
    print(f"  MAE {mae:.3f} | MSE {mse:.3f} | RMSE {rmse:.3f} | R² {r2:.3f}")
    print("Se a validação e o teste dão notas parecidas, a escolha foi confiável.")
    print("A Random Search testa menos combinações: é mais rápida, mas pode perder o melhor modelo.")


if __name__ == "__main__":
    executar_previsao()
    avaliar_desempenho()
