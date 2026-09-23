import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

dados = pd.read_csv("dados_aurora_siger.csv")


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
        dados["erro_absoluto"] / dados["latencia_prevista"]
    ) * 100

    # Classificação do erro
    def classificar_erro(valor):

        if valor < 10:
            return "Normal"

        elif valor < 25:
            return "Atencao"

        else:
            return "Critico"

    dados["situacao_erro"] = dados["erro_relativo"].apply(classificar_erro)

def executar_modelo_previsao():

    print("\n========================================")
    print("         MODELO DE PREVISÃO")
    print("========================================")

    # Variáveis utilizadas para prever a latência observada
    X = dados[
        [
            "latencia_prevista",
            "tensao",
            "corrente"
        ]
    ]

    # Valor que queremos prever
    y = dados["latencia_observada"]

    # Separação dos dados em treino e teste
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Criação do modelo
    modelo = LinearRegression()

    # Treinamento
    modelo.fit(X_treino, y_treino)

    # Previsões
    previsoes = modelo.predict(X_teste)

    print("\nModelo treinado com sucesso!")

    print(f"\nRegistros utilizados no treino: {len(X_treino)}")
    print(f"Registros utilizados no teste: {len(X_teste)}")

    print("\n========================================")
    print("       PREVISÃO X VALOR REAL")
    print("========================================")

    resultado = pd.DataFrame({
        "Latencia Real": y_teste.values,
        "Latencia Prevista pelo Modelo": previsoes
    })

    resultado["Latencia Prevista pelo Modelo"] = (
        resultado["Latencia Prevista pelo Modelo"].round(2)
    )

    print("\n")
    print(resultado.to_string(index=False))

    # ==========================================
    # EXIBIÇÃO DOS RESULTADOS
    # ==========================================

    print("\nResultado da análise:\n")

    resultado = dados[
        [
            "modulo",
            "latencia_prevista",
            "latencia_observada",
            "erro_absoluto",
            "erro_relativo",
            "situacao_erro"
        ]
    ].copy()

    resultado["erro_relativo"] = resultado["erro_relativo"].round(2)

    print(resultado.to_string(index=False))

    # ==========================================
    # INDICADORES GERAIS
    # ==========================================

    media_erro_absoluto = dados["erro_absoluto"].mean()

    media_erro_relativo = dados["erro_relativo"].mean()

    maior_erro = dados["erro_absoluto"].max()

    indice_maior_erro = dados["erro_absoluto"].idxmax()

    modulo_critico = dados.loc[
        indice_maior_erro,
        "modulo"
    ]

    # Contagem das situações
    quantidade_normal = (
        dados["situacao_erro"] == "Normal"
    ).sum()

    quantidade_atencao = (
        dados["situacao_erro"] == "Atencao"
    ).sum()

    quantidade_critico = (
        dados["situacao_erro"] == "Critico"
    ).sum()

    # ==========================================
    # RESUMO
    # ==========================================

    print("\n========================================")
    print("          RESUMO DOS INDICADORES")
    print("========================================")

    print(
        f"Média do erro absoluto: "
        f"{media_erro_absoluto:.2f} ms"
    )

    print(
        f"Média do erro relativo: "
        f"{media_erro_relativo:.2f}%"
    )

    print(
        f"Maior erro absoluto: "
        f"{maior_erro:.2f} ms"
    )

    print(
        f"Módulo com maior erro: "
        f"{modulo_critico}"
    )

    print("\nClassificação dos módulos:")

    print(
        f"Normal: {quantidade_normal}"
    )

    print(
        f"Atenção: {quantidade_atencao}"
    )

    print(
        f"Crítico: {quantidade_critico}"
    )

    print("========================================")