import sys

# Os módulos carregam o CSV ao serem importados. Se o arquivo não existir,
# o sistema avisa o usuário e encerra, em vez de mostrar um erro técnico.
try:
    from modulos.dados import visualizar_dados, consultar_modulo
    from modulos.analises import (
        calcular_indicadores,
        executar_modelo_previsao,
        avaliar_desempenho
    )

except FileNotFoundError:
    print("\nArquivo de dados não encontrado.")
    print("Verifique se 'dados_aurora_siger.csv' está na pasta do projeto.")
    sys.exit(1)

except ModuleNotFoundError as erro:
    print(f"Dependência ausente: {erro.name}. Instale com: python -m pip install -r requirements.txt")
    sys.exit(1)
except (ValueError, OSError) as erro:
    print(f"Não foi possível carregar o CSV: {erro}")
    sys.exit(1)


# ==========================================
# TRATAMENTO DE ERROS DAS ANÁLISES
# ==========================================

def executar_analise(funcao):

    try:
        funcao()

    except KeyError as erro:
        print("\nNão foi possível concluir a análise.")
        print("Verifique se o arquivo CSV possui todas as colunas necessárias.")
        print(f"Detalhe técnico: {erro}")

    except ValueError as erro:
        print("\nNão foi possível concluir a análise.")
        print("Confira os valores informados e os dados do CSV.")
        print(f"Detalhe técnico: {erro}")

    except Exception as erro:
        print("\nOcorreu um erro inesperado.")
        print(f"Detalhe técnico: {erro}")


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

        opcao = input("Digite uma opção: ").strip()

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

        opcao = input("Digite uma opção: ").strip()

        match opcao:

            case "1":
                executar_analise(calcular_indicadores)

            case "2":
                executar_analise(executar_modelo_previsao)

            case "3":
                executar_analise(avaliar_desempenho)

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

        opcao = input("Digite uma opção: ").strip()

        match opcao:

            case "1":
                print("\nPriorização com Heap: próxima etapa do projeto.")

            case "2":
                print("\nBusca com Trie: próxima etapa do projeto.")

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

        opcao = input("Digite uma opção: ").strip()

        match opcao:

            case "1":
                print("\nDispositivos de entrada e saída: próxima etapa do projeto.")

            case "2":
                print("\nConversão de bases: próxima etapa do projeto.")

            case "3":
                print("\nCálculo de potência: próxima etapa do projeto.")

            case "4":
                print("\nGerenciamento inteligente: próxima etapa do projeto.")

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

    print("\nAnálise final integrada: próxima etapa do projeto.")


# ==========================================
# MENU PRINCIPAL
# ==========================================

def main():
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

        opcao = input("Digite uma opção: ").strip()

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
                executar_analise(analise_final)

            case "0":
                print("\nEncerrando o SCIC...")
                print("Sistema finalizado.")
                break

            case _:
                print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSistema encerrado pelo usuário.")
