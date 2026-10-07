"""
Gráficos do SCIC, salvos como imagens PNG em graficos_ou_imagens/ (menu: Análises > opção 7).
Usa Matplotlib (gráficos básicos) e Seaborn (gráficos estatísticos mais bonitos).
"""

import os

import matplotlib

matplotlib.use("Agg")  # "Agg" só salva arquivos, não abre janela (funciona em qualquer computador)
import matplotlib.pyplot as plt
import seaborn as sns

from modulos.inserir_dados import LIMITE_ALERTA, LIMITE_ATENCAO, PASTA, carregar_csv

PASTA_GRAFICOS = os.path.join(PASTA, "graficos_ou_imagens")


def salvar(nome_do_arquivo):
    """Salva a figura atual na pasta de gráficos, fecha ela e devolve o caminho do arquivo."""
    caminho = os.path.join(PASTA_GRAFICOS, nome_do_arquivo)
    plt.tight_layout()  # ajusta as margens para nada ficar cortado
    plt.savefig(caminho, dpi=120)
    plt.close()  # libera a memória da figura
    return caminho


def gerar_graficos():
    dados = carregar_csv()
    if dados is None:
        return
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    sns.set_theme(style="whitegrid")  # visual limpo com grade de fundo
    arquivos = []

    # Gráfico 1 (Matplotlib): latência observada x prevista ao longo dos ciclos
    media_por_ciclo = dados.groupby("ciclo")[["latencia_observada", "latencia_prevista"]].mean()
    plt.figure(figsize=(8, 4.5))
    plt.plot(media_por_ciclo.index, media_por_ciclo["latencia_observada"], marker="o", label="Observada")
    plt.plot(media_por_ciclo.index, media_por_ciclo["latencia_prevista"], marker="s", label="Prevista")
    plt.title("Latência média por ciclo - Aurora Siger")
    plt.xlabel("Ciclo")
    plt.ylabel("Latência (ms)")
    plt.legend()
    arquivos.append(salvar("latencia_por_ciclo.png"))

    # Gráfico 2 (Matplotlib): erro relativo médio por módulo, com as linhas dos limites
    erro_por_modulo = dados.groupby("nome")["erro_relativo_pct"].mean().sort_values(ascending=False)
    plt.figure(figsize=(8, 4.5))
    plt.bar(erro_por_modulo.index, erro_por_modulo.values, color="#E8590C")
    plt.axhline(LIMITE_ATENCAO, color="orange", linestyle="--", label=f"Atenção ({LIMITE_ATENCAO:.0f}%)")
    plt.axhline(LIMITE_ALERTA, color="red", linestyle="--", label=f"Alerta ({LIMITE_ALERTA:.0f}%)")
    plt.title("Erro relativo médio por módulo")
    plt.ylabel("Erro relativo (%)")
    plt.xticks(rotation=25, ha="right")
    plt.legend()
    arquivos.append(salvar("erro_relativo_por_modulo.png"))

    # Gráfico 3 (Seaborn): mapa de calor do erro relativo (linhas = módulos, colunas = ciclos).
    # As manchas escuras mostram QUANDO e ONDE a comunicação ficou ruim.
    tabela = dados.pivot_table(index="nome", columns="ciclo", values="erro_relativo_pct")
    plt.figure(figsize=(10, 4.5))
    sns.heatmap(tabela, cmap="YlOrRd", cbar_kws={"label": "Erro relativo (%)"})
    plt.title("Mapa de calor: erro relativo por módulo e ciclo")
    plt.xlabel("Ciclo")
    plt.ylabel("")
    arquivos.append(salvar("mapa_calor_erro.png"))

    # Gráfico 4 (Seaborn): distribuição da latência de cada módulo (boxplot).
    # A caixa mostra onde fica a maioria dos valores; os pontos soltos são os picos.
    plt.figure(figsize=(9, 4.5))
    sns.boxplot(data=dados, x="nome", y="latencia_observada", color="#74C0FC")
    plt.title("Distribuição da latência observada por módulo")
    plt.xlabel("")
    plt.ylabel("Latência (ms)")
    plt.xticks(rotation=25, ha="right")
    arquivos.append(salvar("distribuicao_latencia.png"))

    print("\nGráficos salvos:")
    for caminho in arquivos:
        print(f"  - {caminho}")


if __name__ == "__main__":
    gerar_graficos()
