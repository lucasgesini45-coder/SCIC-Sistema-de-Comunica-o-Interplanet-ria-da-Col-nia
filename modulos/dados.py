import pandas as pd

dados = pd.read_csv("dados_aurora_siger.csv")


def visualizar_dados():
    print("\n========== DADOS DA COLÔNIA ==========\n")
    print(dados)


def consultar_modulo():
    print("\n========== CONSULTAR MÓDULO ==========")

    nome = input("Digite o nome do módulo: ")

    resultado = dados[
        dados["modulo"].str.contains(nome, case=False, na=False)
    ]

    if resultado.empty:
        print("\nNenhum módulo encontrado.")
    else:
        print("\nResultado encontrado:\n")
        print(resultado)