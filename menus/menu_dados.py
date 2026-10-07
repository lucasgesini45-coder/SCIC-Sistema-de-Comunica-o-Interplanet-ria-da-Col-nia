"""Submenu 1: dados e consultas."""

from modulos.dados import visualizar_dados, consultar_modulo
from modulos.inserir_dados import cadastrar_modulos
from simulacao.simulacao import gerar_dados_simulados


def menu_dados():
    while True:
        print("\n========================================")
        print("          DADOS E CONSULTAS")
        print("========================================\n")
        print("1 - Visualizar dados da colônia")
        print("2 - Consultar módulo")
        print("3 - Cadastrar módulo manualmente")
        print("4 - Gerar dados simulados")
        print("0 - Voltar\n")
        opcao = input("Digite uma opção de 0 a 4:\n-->")

        # match/case é como um "se/senão" mais organizado (precisa do Python 3.10+)
        match opcao:
            case "1":
                visualizar_dados()
            case "2":
                consultar_modulo()
            case "3":
                cadastrar_modulos()
            case "4":
                gerar_dados_simulados()
            case "0":
                break
            case _:
                print("\nOpção inválida. Tente novamente.")
