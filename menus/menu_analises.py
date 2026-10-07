"""Submenu 2: indicadores, previsão, avaliação, otimização do modelo, precisão numérica, Euler e gráficos."""

from calculos.indicadores import calcular_indicadores
from calculos.regressao import executar_previsao, avaliar_desempenho, busca_de_hiperparametros
from calculos.simulacao_euler import simular_recuperacao
from calculos.ponto_flutuante import precisao_numerica
from calculos.graficos import gerar_graficos


def menu_analises():
    while True:
        print("\n========================================")
        print("        ANÁLISES E PREVISÃO")
        print("========================================")
        print("1 - Calcular indicadores e erros")
        print("2 - Executar modelo de previsão")
        print("3 - Avaliar desempenho do modelo")
        print("4 - Escolher o melhor modelo (Grid e Random Search)")
        print("5 - Precisão numérica e ponto flutuante")
        print("6 - Simular recuperação da latência (método de Euler)")
        print("7 - Gerar gráficos (Matplotlib e Seaborn)")
        print("0 - Voltar")
        print("========================================")
        opcao = input("Digite uma opção de 0 a 7:\n-->")

        match opcao:
            case "1":
                # try/except: se algo der errado, o sistema avisa e continua funcionando
                try:
                    calcular_indicadores()
                except KeyError as erro:
                    print("\nErro ao calcular os indicadores.")
                    print("Verifique se o arquivo CSV possui todas as colunas necessárias.")
                    print(f"Detalhe: {erro}")
                except FileNotFoundError:
                    print("\nArquivo de dados não encontrado.")
                    print("Verifique se o arquivo 'dados_aurora_siger.csv' está na pasta do projeto.")
                except Exception as erro:
                    print("\nOcorreu um erro inesperado.")
                    print(f"Detalhe: {erro}")
            case "2":
                try:
                    executar_previsao()
                except Exception as erro:
                    print("\nNão foi possível executar a previsão.")
                    print(f"Detalhe: {erro}")
            case "3":
                try:
                    avaliar_desempenho()
                except Exception as erro:
                    print("\nNão foi possível avaliar o modelo.")
                    print(f"Detalhe: {erro}")
            case "4":
                try:
                    busca_de_hiperparametros()
                except Exception as erro:
                    print("\nNão foi possível comparar os modelos.")
                    print(f"Detalhe: {erro}")
            case "5":
                precisao_numerica()
            case "6":
                try:
                    simular_recuperacao()
                except Exception as erro:
                    print("\nNão foi possível executar a simulação.")
                    print(f"Detalhe: {erro}")
            case "7":
                try:
                    gerar_graficos()
                except Exception as erro:
                    print("\nNão foi possível gerar os gráficos.")
                    print(f"Detalhe: {erro}")
            case "0":
                break
            case _:
                print("\nOpção inválida. Tente novamente.")
