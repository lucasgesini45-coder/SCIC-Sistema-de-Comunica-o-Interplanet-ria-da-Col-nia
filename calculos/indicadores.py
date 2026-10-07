"""Indicadores gerais de latência e de erro (menu: Análises e previsão > opção 1)."""

from modulos.inserir_dados import LIMITE_ALERTA, LIMITE_ATENCAO, carregar_csv


def calcular_indicadores():
    dados = carregar_csv()
    if dados is None:
        return

    print("\n--- Indicadores e erros ---")
    print(
        f"{len(dados)} registros | {dados['nome'].nunique()} módulo(s) | "
        f"{dados['ciclo'].nunique()} ciclo(s)"
    )

    # --- Latência: o tempo que a mensagem leva, em milissegundos ---
    observada = dados["latencia_observada"]
    prevista = dados["latencia_prevista"]
    print("\nLatência (ms):")
    print(f"  Observada: média {observada.mean():.2f} | mínima {observada.min():.2f} | máxima {observada.max():.2f}")
    print(f"  Prevista:  média {prevista.mean():.2f}")

    # --- Erros: quanto o observado se afastou do previsto ---
    erro_absoluto = dados["erro_absoluto"]  # em ms
    erro_relativo = dados["erro_relativo_pct"]  # em %
    print("\nErros:")
    print(f"  Erro absoluto médio: {erro_absoluto.mean():.2f} ms (maior: {erro_absoluto.max():.2f} ms)")
    print(f"  Erro relativo médio: {erro_relativo.mean():.2f}% (maior: {erro_relativo.max():.2f}%)")

    # idxmax devolve a posição da linha onde o erro relativo é o maior
    pior = dados.loc[erro_relativo.idxmax()]
    print(f"  Maior erro relativo: {pior['nome']} ({pior['codigo_sensor']}), ciclo {int(pior['ciclo'])}")

    # --- Quantos registros passaram dos limites ---
    fora_do_aceitavel = int((erro_relativo > LIMITE_ATENCAO).sum())
    criticos = int((erro_relativo > LIMITE_ALERTA).sum())
    print(f"\nAcima de {LIMITE_ATENCAO:.0f}% (fora do aceitável): {fora_do_aceitavel} registro(s) ({fora_do_aceitavel / len(dados) * 100:.1f}%)")
    print(f"Acima de {LIMITE_ALERTA:.0f}% (crítico): {criticos} registro(s) ({criticos / len(dados) * 100:.1f}%)")

    # --- Uma linha por módulo, do que mais erra para o que menos erra ---
    tabela = (
        dados.groupby("nome")
        .agg(
            erro_rel_medio=("erro_relativo_pct", "mean"),
            erro_rel_max=("erro_relativo_pct", "max"),
            lat_obs_media=("latencia_observada", "mean"),
        )
        .round(2)
        .sort_values("erro_rel_medio", ascending=False)
    )
    print("\nPor módulo (ordenado pelo erro relativo médio):")
    print(tabela.to_string())
