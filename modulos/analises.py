import math
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from modulos.dados import dados

# Variáveis usadas pelo modelo
COLUNAS_ENTRADA = ["latencia_prevista", "tensao", "corrente"]
COLUNA_SAIDA = "latencia_observada"


# ==========================================
# CLASSIFICAÇÃO DO ERRO
# ==========================================

def classificar_erro(valor):

    if pd.isna(valor):
        return "Indefinido"

    if valor < 10:
        return "Normal"

    elif valor < 25:
        return "Atencao"

    else:
        return "Critico"


# ==========================================
# INDICADORES E ERROS
# ==========================================

def calcular_indicadores():

    print("\n========================================")
    print("       INDICADORES E ERROS")
    print("========================================")

    # Calculando o erro absoluto
    dados["erro_absoluto"] = abs(
        dados["latencia_observada"] - dados["latencia_prevista"]
    )

    # Calculando o erro relativo
    dados["erro_relativo"] = (
        dados["erro_absoluto"] / dados["latencia_prevista"].replace(0, float("nan"))
    ) * 100

    # Classificação de cada registro
    dados["situacao_erro"] = dados["erro_relativo"].apply(classificar_erro)

    # ------------------------------------------
    # Tabela com o resultado de cada registro
    # ------------------------------------------

    print("\nResultado da análise:\n")

    resultado = dados[
        [
            "modulo",
            "ciclo",
            "latencia_prevista",
            "latencia_observada",
            "erro_absoluto",
            "erro_relativo",
            "situacao_erro"
        ]
    ].copy()

    resultado["erro_relativo"] = resultado["erro_relativo"].round(2)

    print(resultado.to_string(index=False))

    # ------------------------------------------
    # Indicadores gerais
    # ------------------------------------------

    media_erro_absoluto = dados["erro_absoluto"].mean()
    media_erro_relativo = dados["erro_relativo"].mean()

    maior_erro = dados["erro_absoluto"].max()
    indice_maior_erro = dados["erro_absoluto"].idxmax()
    modulo_critico = dados.loc[indice_maior_erro, "modulo"]

    quantidade_normal = (dados["situacao_erro"] == "Normal").sum()
    quantidade_atencao = (dados["situacao_erro"] == "Atencao").sum()
    quantidade_critico = (dados["situacao_erro"] == "Critico").sum()

    print("\n========================================")
    print("          RESUMO DOS INDICADORES")
    print("========================================")

    print(f"Média do erro absoluto: {media_erro_absoluto:.2f} ms")
    print(f"Média do erro relativo: {media_erro_relativo:.2f}%")
    print(f"Maior erro absoluto: {maior_erro:.2f} ms")
    print(f"Módulo com maior erro: {modulo_critico}")

    print("\nClassificação dos registros:")
    print(f"Normal: {quantidade_normal}")
    print(f"Atenção: {quantidade_atencao}")
    print(f"Crítico: {quantidade_critico}")
    print("Indefinido (latência prevista zero):", dados["situacao_erro"].eq("Indefinido").sum())

    print("========================================")


# ==========================================
# TREINAMENTO DO MODELO
# ==========================================

def treinar_modelo():

    # Variáveis utilizadas para prever a latência observada
    if len(dados) < 10:
        raise ValueError("São necessários pelo menos 10 registros para treino e avaliação.")
    X = dados[COLUNAS_ENTRADA]

    # Valor que queremos prever
    y = dados[COLUNA_SAIDA]

    # Separação dos dados em treino (80%) e teste (20%)
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Criação e treinamento do modelo
    modelo = LinearRegression()
    modelo.fit(X_treino, y_treino)

    # Previsões para os registros de teste
    previsoes = modelo.predict(X_teste)

    return X_treino, X_teste, y_teste, previsoes


# ==========================================
# MODELO DE PREVISÃO
# ==========================================

def executar_modelo_previsao():

    print("\n========================================")
    print("         MODELO DE PREVISÃO")
    print("========================================")

    X_treino, X_teste, y_teste, previsoes = treinar_modelo()

    print("\nModelo treinado com sucesso!")

    print(f"\nRegistros utilizados no treino: {len(X_treino)}")
    print(f"Registros utilizados no teste: {len(X_teste)}")

    print("\n========================================")
    print("       PREVISÃO X VALOR REAL")
    print("========================================\n")

    resultado = pd.DataFrame({
        "Modulo": dados.loc[X_teste.index, "modulo"].values,
        "Latencia Real": y_teste.values,
        "Latencia Prevista pelo Modelo": previsoes.round(2)
    })

    resultado["Diferenca"] = (
        resultado["Latencia Prevista pelo Modelo"] - resultado["Latencia Real"]
    ).round(2)

    print(resultado.to_string(index=False))

    print("\nPara medir a qualidade do modelo, use a opção 3.")


# ==========================================
# AVALIAÇÃO DO MODELO
# ==========================================

def avaliar_desempenho():

    print("\n========================================")
    print("       AVALIAÇÃO DO MODELO")
    print("========================================")

    X_treino, X_teste, y_teste, previsoes = treinar_modelo()

    # Erro médio das previsões do modelo
    erro_modelo = mean_absolute_error(y_teste, previsoes)

    # Erro médio da latência prevista original, nos mesmos registros
    erro_original = mean_absolute_error(y_teste, X_teste["latencia_prevista"])

    # Coeficiente de determinação (quanto da variação o modelo explica)
    r2 = r2_score(y_teste, previsoes)

    reducao = (1 - erro_modelo / erro_original) * 100 if erro_original else float("nan")

    print(f"\nRegistros avaliados (teste): {len(X_teste)}")

    print(f"\nErro médio da previsão original: {erro_original:.2f} ms")
    print(f"Erro médio do modelo:            {erro_modelo:.2f} ms")
    print(f"Redução do erro:                 {reducao:.1f}%" if math.isfinite(reducao)
          else "Redução percentual indefinida: erro original igual a zero.")

    print(f"\nR² do modelo: {r2:.2f}")

    print("\nInterpretação:")

    if erro_modelo < erro_original:
        print("O modelo prevê a latência melhor que a estimativa original.")
    else:
        print("O modelo ainda não supera a estimativa original.")

    print(
        f"Com {len(dados)} registros, esta avaliação é exploratória. "
        "Mais dados e validação temporal são necessários para avaliar generalização."
    )

    print("========================================")
