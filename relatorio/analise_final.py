"""
Análise final do SCIC: junta os principais resultados em um resumo
mostrado no terminal e salvo em resumo_analise_final.txt.
"""

import os
from datetime import datetime

from alertas.alertas import top_alertas
from calculos.regressao import calcular_metricas
from modulos.inserir_dados import LIMITE_ATENCAO, PASTA, STATUS, carregar_csv

ARQUIVO_RESUMO = os.path.join(PASTA, "resumo_analise_final.txt")


def montar_resumo(dados):
    """Monta o texto do resumo, linha por linha, e devolve tudo junto."""
    linhas = []
    linhas.append("=" * 60)
    linhas.append("   ANÁLISE FINAL - SCIC / AURORA SIGER")
    linhas.append(f"   Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append("=" * 60)
    linhas.append(
        f"Base: {len(dados)} registros | {dados['nome'].nunique()} módulos | "
        f"{dados['ciclo'].nunique()} ciclos"
    )

    # 1) Situação geral: quantos registros em cada status
    linhas.append("\n1) Situação dos registros")
    contagem = dados["status"].value_counts()
    for status in STATUS:
        quantidade = int(contagem.get(status, 0))
        linhas.append(f"   {status:<11}: {quantidade:>4} ({quantidade / len(dados) * 100:.1f}%)")

    # 2) Latência
    observada = dados["latencia_observada"]
    linhas.append("\n2) Latência (ms)")
    linhas.append(
        f"   Observada: média {observada.mean():.2f} | mín {observada.min():.2f} | máx {observada.max():.2f}"
    )
    linhas.append(f"   Prevista:  média {dados['latencia_prevista'].mean():.2f}")

    # 3) Erros numéricos
    erro_relativo = dados["erro_relativo_pct"]
    pior = dados.loc[erro_relativo.idxmax()]
    acima_do_limite = int((erro_relativo > LIMITE_ATENCAO).sum())
    linhas.append("\n3) Erros numéricos")
    linhas.append(f"   Erro absoluto médio: {dados['erro_absoluto'].mean():.2f} ms")
    linhas.append(f"   Erro relativo médio: {erro_relativo.mean():.2f}%")
    linhas.append(f"   Maior erro relativo: {pior['codigo_sensor']} ({erro_relativo.max():.2f}%)")
    linhas.append(f"   Registros acima de {LIMITE_ATENCAO:.0f}%: {acima_do_limite}")

    # 4) Eletricidade
    potencia_kw = dados["potencia"] / 1000  # a coluna está em W; aqui mostramos em kW
    linhas.append("\n4) Eletricidade")
    linhas.append(f"   Potência média por leitura: {potencia_kw.mean():.3f} kW")
    linhas.append(f"   Maior potência: {dados.loc[potencia_kw.idxmax(), 'codigo_sensor']}")

    # 5) Desempenho: compara a latência prevista gravada no CSV com a observada
    mae, mse, rmse, r2 = calcular_metricas(dados["latencia_observada"], dados["latencia_prevista"])
    linhas.append("\n5) Desempenho da previsão registrada na base")
    linhas.append(f"   MAE {mae:.3f} | MSE {mse:.3f} | RMSE {rmse:.3f} | R² {r2:.3f}")
    if mae > 0 and rmse / mae > 1.5:
        linhas.append("   RMSE bem maior que MAE: há erros grandes isolados.")

    # 6) Alertas mais urgentes, na ordem do heap
    alertas = top_alertas(dados, 5)
    linhas.append("\n6) Alertas mais urgentes (heap)")
    if alertas:
        for posicao, alerta in enumerate(alertas, 1):
            linhas.append(
                f"   {posicao}. {alerta['nome']} | {alerta['codigo_sensor']} | {alerta['mensagem_alerta']}"
            )
    else:
        linhas.append("   Nenhum alerta ativo.")

    # 7) Recomendação final, sempre com a equipe humana no controle
    linhas.append("\n7) Recomendação")
    if alertas:
        linhas.append(f"   Verificar primeiro o dispositivo {alertas[0]['codigo_sensor']}.")
    else:
        linhas.append("   Operação dentro do limite aceitável.")
    linhas.append("   Decisões automatizadas devem ser validadas pela equipe humana.")
    linhas.append("=" * 60)
    return "\n".join(linhas)


def gerar_analise_final():
    """Mostra o resumo no terminal e salva uma cópia em arquivo de texto."""
    dados = carregar_csv()
    if dados is None:
        return
    resumo = montar_resumo(dados)
    print("\n" + resumo)
    with open(ARQUIVO_RESUMO, "w", encoding="utf-8") as arquivo:
        arquivo.write(resumo)
    print(f"\nResumo salvo em: {ARQUIVO_RESUMO}")


if __name__ == "__main__":
    gerar_analise_final()
