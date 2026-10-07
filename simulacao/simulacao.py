"""
Gera dados simulados da Aurora Siger, para quem não quiser digitar tudo à mão.

Cada módulo tem uma latência "de referência" calculada por uma fórmula simples.
Depois a latência observada recebe um pouco de ruído aleatório, alguns picos
ocasionais e, em um módulo, uma piora gradual (para a manutenção preditiva ter o que detectar).
"""

import os
import shutil

import numpy as np
import pandas as pd

from modulos.inserir_dados import (
    ARQUIVO_CSV,
    COLUNAS,
    LIMITE_ALERTA,
    LIMITE_ATENCAO,
    ler_inteiro,
)

# Semente fixa: assim os dados saem sempre iguais para o mesmo número de ciclos
SEMENTE = 42

# Cada linha: (nome, tipo, código do sensor, latência base, fator de potência,
#              tensão nominal, corrente nominal, prioridade de 1 a 5)
MODULOS = [
    ("Centro de Comunicação", "Comunicação", "SEN-A1F", 250, 1.60, 28, 4.0, 5),
    ("Suporte Médico Alfa", "Suporte médico", "SEN-B2C", 180, 1.10, 24, 2.5, 5),
    ("Laboratório Boreal", "Laboratório", "SEN-C3D", 220, 1.30, 24, 3.0, 3),
    ("Estufa Aurora", "Agricultura", "SEN-D4E", 170, 1.00, 12, 3.5, 4),
    ("Habitação Norte", "Habitação", "SEN-E5F", 150, 0.80, 24, 2.0, 4),
    ("Armazenamento de Dados", "Armazenamento de dados", "SEN-F60", 300, 1.50, 48, 1.5, 3),
]

# Posição (na lista acima) do módulo que vai piorando com o tempo: a Estufa Aurora
INDICE_DO_MODULO_QUE_DEGRADA = 3

MENSAGENS = {
    "Ativo": "Operação normal",
    "Atenção": "Latência acima do previsto",
    "Alerta": "Latência crítica no enlace",
    "Manutenção": "Manutenção programada",
    "Inativo": "Sem comunicação com o módulo",
}


def gerar_dataframe(n_ciclos, semente=SEMENTE):
    """Cria a tabela completa de registros: 6 módulos x n_ciclos."""
    gerador = np.random.default_rng(semente)
    # Conta quantos ciclos seguidos cada sensor ficou fora do limite
    persistencia = {modulo[2]: 0 for modulo in MODULOS}
    linhas = []

    for ciclo in range(1, n_ciclos + 1):
        for posicao, (nome, tipo, codigo, base, fator, tensao_nominal, corrente_nominal, prioridade) in enumerate(MODULOS):

            # Tensão e corrente oscilam um pouco em torno do valor nominal
            tensao = round(tensao_nominal * (1 + gerador.normal(0, 0.04)), 2)
            corrente = round(corrente_nominal * (1 + gerador.normal(0, 0.12)), 2)
            potencia = round(tensao * corrente, 4)  # P = V x I

            # Latência esperada: base + efeito da potência + pequeno aumento por ciclo
            prevista = base + fator * potencia + 1.5 * ciclo

            # Desvio normal (ruído) e, de vez em quando (12%), um pico maior
            desvio = gerador.normal(0, 0.04)
            if gerador.random() < 0.12:
                desvio += gerador.uniform(0.15, 0.55)
            # O módulo "doente" piora um pouquinho a cada ciclo
            if posicao == INDICE_DO_MODULO_QUE_DEGRADA:
                desvio += 0.012 * ciclo

            observada = max(1.0, prevista * (1 + desvio))
            prevista, observada = round(prevista, 2), round(observada, 2)

            # Erro absoluto e relativo (relativo = erro / prevista, em %)
            erro_absoluto = round(abs(observada - prevista), 4)
            erro_relativo = round(erro_absoluto / prevista * 100, 2)

            # O status depende de quão grande é o erro relativo
            if erro_relativo > LIMITE_ALERTA:
                status = "Alerta"
            elif erro_relativo > LIMITE_ATENCAO:
                status = "Atenção"
            else:
                status = "Ativo"
            # Em uma pequena parte dos casos o módulo está em manutenção ou inativo
            sorteio = gerador.random()
            if sorteio < 0.03:
                status = "Manutenção"
            elif sorteio < 0.05:
                status = "Inativo"

            # Persistência: ciclos seguidos fora do limite (zera quando volta ao normal)
            if erro_relativo > LIMITE_ATENCAO:
                persistencia[codigo] += 1
            else:
                persistencia[codigo] = 0

            linhas.append(
                {
                    "ciclo": ciclo,
                    "nome": nome,
                    "tipo": tipo,
                    "codigo_sensor": codigo,
                    "latencia_observada": observada,
                    "latencia_prevista": prevista,
                    "erro_absoluto": erro_absoluto,
                    "erro_relativo_pct": erro_relativo,
                    "tensao": tensao,
                    "corrente": corrente,
                    "potencia": potencia,
                    "status": status,
                    "prioridade": prioridade,
                    "persistencia": persistencia[codigo],
                    "mensagem_alerta": MENSAGENS[status],
                }
            )
    return pd.DataFrame(linhas, columns=COLUNAS)


def gerar_dados_simulados():
    """Pergunta quantos ciclos simular e salva o resultado no CSV (com backup, se já existir)."""
    print("\n--- Gerar Dados Simulados ---")
    print(f"Serão simulados {len(MODULOS)} módulos da Aurora Siger por vários ciclos.")
    n_ciclos = ler_inteiro("Quantos ciclos simular? (5 a 60): ", 5, 60)

    # Se já existe um CSV, pergunta antes de apagar e guarda uma cópia de segurança
    if os.path.exists(ARQUIVO_CSV):
        print(f"\nJá existe um arquivo de dados: {ARQUIVO_CSV}")
        print("1. Substituir (o arquivo atual vira um backup)")
        print("2. Cancelar")
        if ler_inteiro("--> ", 1, 2) == 2:
            print("Operação cancelada. Nenhum dado foi alterado.")
            return
        arquivo_backup = ARQUIVO_CSV.replace(".csv", "_backup.csv")
        shutil.copyfile(ARQUIVO_CSV, arquivo_backup)
        print(f"Backup salvo em {arquivo_backup}")

    dados = gerar_dataframe(n_ciclos)
    dados.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8")

    contagem = dados["status"].value_counts()
    print(f"\n{len(dados)} registros gerados e salvos em {ARQUIVO_CSV}.")
    print("Status gerados: " + ", ".join(f"{status}: {qtd}" for status, qtd in contagem.items()))
    print(f"Semente fixa = {SEMENTE} (os dados são sempre os mesmos para o mesmo nº de ciclos).")


if __name__ == "__main__":
    gerar_dados_simulados()
