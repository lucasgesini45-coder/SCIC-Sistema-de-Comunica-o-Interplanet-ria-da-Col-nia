import os
import numpy as np

import pandas as pd

# Mostra todas as colunas no terminal, sem cortar com "..."
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", None)

# Caminho do CSV a partir da pasta do projeto, para o sistema funcionar
# mesmo quando o terminal é aberto em outra pasta.
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_CSV = os.path.join(PASTA_PROJETO, "dados_aurora_siger.csv")

COLUNAS = ["id", "modulo", "tipo", "latencia_prevista", "latencia_observada",
           "tensao", "corrente", "status", "prioridade", "codigo_sensor", "mensagem", "ciclo"]
NUMERICAS = ["id", "latencia_prevista", "latencia_observada", "tensao", "corrente", "prioridade", "ciclo"]


def carregar_dados(caminho=CAMINHO_CSV):
    """Carrega e valida a base antes de disponibilizá-la aos módulos."""
    tabela = pd.read_csv(caminho)
    faltantes = set(COLUNAS) - set(tabela.columns)
    if faltantes:
        raise ValueError(f"Colunas ausentes: {', '.join(sorted(faltantes))}")
    if tabela.empty:
        raise ValueError("O CSV não pode estar vazio.")
    for coluna in NUMERICAS:
        tabela[coluna] = pd.to_numeric(tabela[coluna], errors="raise")
        if not np.isfinite(tabela[coluna]).all() or (tabela[coluna] < 0).any():
            raise ValueError(f"A coluna {coluna} deve conter números finitos e não negativos.")
    for coluna in ["id", "prioridade", "ciclo"]:
        if (tabela[coluna] % 1 != 0).any():
            raise ValueError(f"A coluna {coluna} deve conter números inteiros.")
        tabela[coluna] = tabela[coluna].astype(int)
    if tabela["id"].duplicated().any() or (tabela["id"] < 1).any():
        raise ValueError("Os IDs devem ser positivos e únicos.")
    if not tabela["prioridade"].isin([1, 2, 3]).all():
        raise ValueError("Prioridade deve ser 1, 2 ou 3 (3 = maior urgência).")
    if (tabela["ciclo"] < 1).any():
        raise ValueError("O ciclo deve ser positivo.")
    for coluna in set(COLUNAS) - set(NUMERICAS):
        if tabela[coluna].isna().any() or tabela[coluna].astype(str).str.strip().eq("").any():
            raise ValueError(f"A coluna {coluna} contém texto vazio.")
        tabela[coluna] = tabela[coluna].astype(str).str.strip()
    return tabela


dados = carregar_dados()


def visualizar_dados():
    print("\n========== DADOS DA COLÔNIA ==========\n")
    print(dados.to_string(index=False))


def consultar_modulo():
    print("\n========== CONSULTAR MÓDULO ==========")

    nome = input("Digite o nome do módulo: ").strip()
    if not nome:
        print("Informe parte do nome de um módulo.")
        return

    resultado = dados[
        dados["modulo"].str.contains(nome, case=False, na=False, regex=False)
    ]

    if resultado.empty:
        print("\nNenhum módulo encontrado.")
    else:
        print(f"\n{len(resultado)} registro(s) encontrado(s):\n")
        print(
            resultado[
                [
                    "id",
                    "modulo",
                    "ciclo",
                    "latencia_prevista",
                    "latencia_observada",
                    "status",
                    "prioridade",
                    "mensagem"
                ]
            ].to_string(index=False)
        )
