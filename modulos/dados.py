"""Mostrar e consultar os dados da colônia (arquivo dados_aurora_siger.csv)."""

import pandas as pd

from modulos.inserir_dados import carregar_csv, ler_texto

# Colunas que aparecem na tabela resumida (as outras ficam só no CSV)
COLUNAS_DA_TABELA = [
    "ciclo",
    "nome",
    "codigo_sensor",
    "latencia_observada",
    "latencia_prevista",
    "erro_relativo_pct",
    "potencia",
    "status",
    "prioridade",
]


def visualizar_dados():
    """Mostra um resumo geral dos dados e os 15 últimos registros."""
    dados = carregar_csv()
    if dados is None:
        return

    print(
        f"\n{len(dados)} registros | {dados['nome'].nunique()} módulo(s) | "
        f"{dados['ciclo'].nunique()} ciclo(s)"
    )

    # Quantos registros existem de cada status (Ativo, Atenção, Alerta...)
    print("\nStatus dos registros:")
    print(dados["status"].value_counts().to_string())

    print("\nÚltimos 15 registros:")
    # display.width maior evita que a tabela quebre em várias linhas no terminal
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(dados[COLUNAS_DA_TABELA].tail(15).to_string(index=False))
    if len(dados) > 15:
        print(f"\n(mostrando 15 de {len(dados)}; o arquivo completo é dados_aurora_siger.csv)")


def consultar_modulo():
    """Procura um módulo pelo nome (ou parte dele) e mostra um resumo dele."""
    dados = carregar_csv()
    if dados is None:
        return

    print("\nMódulos cadastrados:")
    for nome in sorted(dados["nome"].unique()):
        print(f"  - {nome}")

    busca = ler_texto("\nDigite o nome (ou parte do nome) do módulo: ")
    # str.contains ignora maiúsculas/minúsculas e aceita só um pedaço do nome
    encontrados = dados[dados["nome"].str.contains(busca, case=False, na=False, regex=False)]
    if encontrados.empty:
        print(f"\nNenhum módulo encontrado com '{busca}'.")
        return

    # Um resumo para cada módulo encontrado
    for nome, registros in encontrados.groupby("nome"):
        ultimo = registros.sort_values("ciclo").iloc[-1]  # leitura mais recente
        print(
            f"\n=== {nome} ({registros['tipo'].iloc[0]}, sensor {registros['codigo_sensor'].iloc[0]}) ==="
        )
        print(f"Registros: {len(registros)} | Prioridade do módulo: {int(registros['prioridade'].iloc[0])}")
        print(
            f"Latência observada média: {registros['latencia_observada'].mean():.2f} ms "
            f"(prevista média: {registros['latencia_prevista'].mean():.2f} ms)"
        )
        print(
            f"Erro relativo médio: {registros['erro_relativo_pct'].mean():.2f}% | "
            f"maior: {registros['erro_relativo_pct'].max():.2f}%"
        )
        print(f"Potência média: {registros['potencia'].mean():.1f} W")
        print(f"Status por ciclo: {registros['status'].value_counts().to_dict()}")
        print(f"Último registro (ciclo {int(ultimo['ciclo'])}): {ultimo['status']} - {ultimo['mensagem_alerta']}")
