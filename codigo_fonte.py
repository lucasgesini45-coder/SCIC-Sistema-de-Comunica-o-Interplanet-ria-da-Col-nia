from modulos.dados import visualizar_dados, consultar_modulo
from modulos.analises import (
    calcular_indicadores,
    executar_modelo_previsao
)


# ==========================================
# SUBMENU - DADOS E CONSULTAS
# ==========================================

def menu_dados():

    while True:

        print("\n========================================")
        print("          DADOS E CONSULTAS")
        print("========================================")

        print("1 - Visualizar dados da colônia")
        print("2 - Consultar módulo")
        print("0 - Voltar")

        print("========================================")

        opcao = input("Digite uma opção: ")

        match opcao:

            case "1":
                visualizar_dados()

            case "2":
                consultar_modulo()

            case "0":
                break

            case _:
                print("\nOpção inválida. Tente novamente.")


# ==========================================
# SUBMENU - ANÁLISES E PREVISÃO
# ==========================================

def menu_analises():

    while True:

        print("\n========================================")
        print("        ANÁLISES E PREVISÃO")
        print("========================================")

        print("1 - Calcular indicadores e erros")
        print("2 - Executar modelo de previsão")
        print("3 - Avaliar desempenho do modelo")
        print("0 - Voltar")

        print("========================================")

        opcao = input("Digite uma opção: ")

        match opcao:

            case "1":
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
                    executar_modelo_previsao()

                except KeyError as erro:
                    print("\n========================================")
                    print("              ATENÇÃO")
                    print("========================================")

                    print("\nNão foi possível executar a previsão.")

                    print(
                        "Algumas informações necessárias ainda "
                        "não foram calculadas."
                    )

                    print(
                        "\nExecute primeiro:"
                        "\n2 - Análises e previsão"
                        "\n1 - Calcular indicadores e erros"
                    )

                    print(f"\nDetalhe técnico: {erro}")

            case "3":
                print("\nAvaliação do modelo será desenvolvida.")

            case "0":
                break

            case _:
                print("\nOpção inválida. Tente novamente.")


# ==========================================
# SUBMENU - ALERTAS E BUSCAS
# ==========================================

def menu_alertas():

    while True:

        print("\n========================================")
        print("          ALERTAS E BUSCAS")
        print("========================================")

        print("1 - Priorizar alertas com Heap")
        print("2 - Buscar registros com Trie")
        print("0 - Voltar")

        print("========================================")

        opcao = input("Digite uma opção: ")

        match opcao:

            case "1":
                print("\nPriorização com Heap será desenvolvida.")

            case "2":
                print("\nBusca com Trie será desenvolvida.")

            case "0":
                break

            case _:
                print("\nOpção inválida. Tente novamente.")


# ==========================================
# SUBMENU - SISTEMAS E ELETRICIDADE
# ==========================================

def menu_sistemas():

    while True:

        print("\n========================================")
        print("      SISTEMAS E ELETRICIDADE")
        print("========================================")

        print("1 - Dispositivos de entrada e saída")
        print("2 - Conversão de bases numéricas")
        print("3 - Cálculo de potência")
        print("4 - Gerenciamento inteligente")
        print("0 - Voltar")

        print("========================================")

        opcao = input("Digite uma opção: ")

        match opcao:

            case "1":
                print("\nFunção de dispositivos será desenvolvida.")

            case "2":
                print("\nConversão de bases será desenvolvida.")

            case "3":
                print("\nCálculo de potência será desenvolvido.")

            case "4":
                print("\nGerenciamento inteligente será desenvolvido.")

            case "0":
                break

            case _:
                print("\nOpção inválida. Tente novamente.")


# ==========================================
# ANÁLISE FINAL
# ==========================================

def analise_final():

    print("\n========================================")
    print("          ANÁLISE FINAL SCIC")
    print("========================================")

    print("\nA análise final será desenvolvida nas próximas etapas.")


# ==========================================
# MENU PRINCIPAL
# ==========================================

while True:

    print("\n==========================================")
    print("          SCIC - AURORA SIGER")
    print(" Sistema de Comunicação Interplanetária")
    print("==========================================")

    print("1 - Dados e consultas")
    print("2 - Análises e previsão")
    print("3 - Alertas e buscas")
    print("4 - Sistemas e eletricidade")
    print("5 - Análise final")
    print("0 - Sair")

    print("==========================================")

    opcao = input("Digite uma opção: ")

    match opcao:

        case "1":
            menu_dados()

        case "2":
            menu_analises()

        case "3":
            menu_alertas()

        case "4":
            menu_sistemas()

        case "5":
            analise_final()

        case "0":
            print("\nEncerrando o SCIC...")
            print("Sistema finalizado.")
            break

        case _:
            print("\nOpção inválida. Tente novamente.")