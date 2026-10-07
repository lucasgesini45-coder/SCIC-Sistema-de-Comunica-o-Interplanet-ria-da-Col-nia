"""
entrada e saida dos dados da colonia

aqui ficam tres coisas:

   1- as constantes do sistema (colunas do csv, status e limites de erro)

   2 - as funcoes que leem o que o usuario digita, com validacao

   3 - as funcoes que salvam e carregam o arquivo dados_aurora_siger.csv
"""

import os

import pandas as pd

# Pasta principal do projeto (a que fica acima de "modulos/"). É lá que mora o CSV.
PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_CSV = os.path.join(PASTA, "dados_aurora_siger.csv")

# Ordem fixa das colunas do CSV. Todo o sistema depende dela.
COLUNAS = [
    "ciclo",
    "nome",
    "tipo",
    "codigo_sensor",
    "latencia_observada",
    "latencia_prevista",
    "erro_absoluto",
    "erro_relativo_pct",
    "tensao",
    "corrente",
    "potencia",
    "status",
    "prioridade",
    "persistencia",
    "mensagem_alerta",
]

# Tipos de módulo e status que o usuário pode escolher no cadastro
TIPOS = [
    "Habitação",
    "Agricultura",
    "Comunicação",
    "Laboratório",
    "Suporte médico",
    "Armazenamento de dados",
]
STATUS = ["Ativo", "Atenção", "Alerta", "Manutenção", "Inativo"]

# Limites do erro relativo (em %), usados para decidir se um desvio preocupa ou não
LIMITE_ATENCAO = 10.0  # passou disso: fora do aceitável -> "Atenção"
LIMITE_ALERTA = 25.0  # passou disso: situação crítica -> "Alerta"


# ------------------------------------------------------------
# Leitura segura do que o usuário digita
# ------------------------------------------------------------
def ler_texto(mensagem):
    """Pede um texto e só aceita se não estiver vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("ERRO! O campo não pode ficar vazio. Tente novamente.\n")


def ler_float(mensagem, minimo=0.0):
    """Pede um número decimal (aceita vírgula) e não deixa passar de um valor mínimo."""
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor < minimo:
                print(f"ERRO! O valor deve ser maior ou igual a {minimo}.\n")
                continue
            return valor
        except ValueError:
            print("ERRO! Digite um número válido.\n")


def ler_inteiro(mensagem, minimo, maximo):
    """Pede um número inteiro dentro de um intervalo (de 'minimo' até 'maximo')."""
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"ERRO! Digite um número inteiro de {minimo} a {maximo}.\n")
        except ValueError:
            print("ERRO! O valor deve ser um número inteiro.\n")


def escolher_opcao(titulo, opcoes):
    """Mostra uma lista numerada e devolve a opção que o usuário escolheu."""
    print(titulo)
    for numero, opcao in enumerate(opcoes, 1):
        print(f"{numero}. {opcao}")
    escolhido = ler_inteiro("--> ", 1, len(opcoes))
    return opcoes[escolhido - 1]


# ------------------------------------------------------------
# Cadastro manual de um módulo
# ------------------------------------------------------------
def inserir_dados():
    """Pergunta os dados de um módulo e devolve um dicionário já com os cálculos feitos."""
    print("\n--- Cadastro Manual de Módulos ---\n")

    nome = ler_texto("Nome do módulo: ")
    tipo = escolher_opcao("\nTipo do módulo:", TIPOS)
    codigo = ler_texto("\nCódigo do dispositivo/sensor (ex: SEN-A1F): ").upper()
    ciclo = ler_inteiro("Ciclo de registro (inteiro >= 1): ", 1, 10**6)

    latencia_observada = ler_float("Latência observada (ms): ")
    # A prevista nunca pode ser zero, senão o erro relativo (que divide por ela) quebra
    latencia_prevista = ler_float("Latência prevista (ms): ", minimo=0.001)

    tensao = ler_float("Tensão (V): ")
    corrente = ler_float("Corrente (A): ")

    status = escolher_opcao("\nStatus do módulo:", STATUS)
    prioridade = ler_inteiro("Prioridade do módulo (1 = baixa a 5 = alta): ", 1, 5)
    persistencia = ler_inteiro(
        "Persistência (ciclos consecutivos fora do limite): ", 0, 10**6
    )
    mensagem = ler_texto("Mensagem resumida do alerta: ")

    # Cálculos feitos automaticamente, para o usuário não precisar digitar
    erro_absoluto = abs(latencia_observada - latencia_prevista)
    erro_relativo = erro_absoluto / latencia_prevista * 100
    potencia = tensao * corrente  # P = V x I

    return {
        "ciclo": ciclo,
        "nome": nome,
        "tipo": tipo,
        "codigo_sensor": codigo,
        "latencia_observada": latencia_observada,
        "latencia_prevista": latencia_prevista,
        "erro_absoluto": round(erro_absoluto, 4),
        "erro_relativo_pct": round(erro_relativo, 2),
        "tensao": tensao,
        "corrente": corrente,
        "potencia": round(potencia, 4),
        "status": status,
        "prioridade": prioridade,
        "persistencia": persistencia,
        "mensagem_alerta": mensagem,
    }


# ------------------------------------------------------------
# Salvar e carregar o CSV
# ------------------------------------------------------------
def csv_compativel():
    """Confere se o CSV que já existe tem as mesmas colunas que o sistema espera."""
    if not os.path.exists(ARQUIVO_CSV):
        return True  # sem arquivo ainda: tudo bem, ele será criado
    colunas_do_arquivo = list(pd.read_csv(ARQUIVO_CSV, nrows=0).columns)
    if colunas_do_arquivo != COLUNAS:
        print(f"\nERRO! O arquivo {ARQUIVO_CSV} tem colunas diferentes das esperadas.")
        print("Renomeie ou apague esse arquivo e tente novamente.")
        return False
    return True


def salvar_modulo(modulo):
    """Acrescenta um módulo no final do CSV (cria o arquivo se ele não existir)."""
    if not csv_compativel():
        return False
    tabela = pd.DataFrame([modulo], columns=COLUNAS)
    arquivo_existe = os.path.exists(ARQUIVO_CSV)
    # mode="a" = acrescentar no fim; o cabeçalho só é escrito na primeira vez
    tabela.to_csv(
        ARQUIVO_CSV, mode="a", header=not arquivo_existe, index=False, encoding="utf-8"
    )
    print(f"\nMódulo '{modulo['nome']}' salvo em {ARQUIVO_CSV}.")
    print(
        f"Erro absoluto: {modulo['erro_absoluto']} ms | "
        f"Erro relativo: {modulo['erro_relativo_pct']}% | "
        f"Potência: {modulo['potencia']} W"
    )
    return True


def carregar_csv(minimo=1):
    """
    Lê o CSV e devolve um DataFrame. Se algo estiver errado (arquivo ausente,
    colunas faltando ou poucos registros), avisa o usuário e devolve None.
    """
    if not os.path.exists(ARQUIVO_CSV):
        print("\nERRO! Nenhum dado encontrado.")
        print("Cadastre módulos ou gere dados simulados em: Dados e consultas.")
        return None

    dados = pd.read_csv(ARQUIVO_CSV)

    colunas_faltando = [coluna for coluna in COLUNAS if coluna not in dados.columns]
    if colunas_faltando:
        print(f"\nERRO! Colunas ausentes no CSV: {', '.join(colunas_faltando)}")
        return None

    if len(dados) < minimo:
        print(
            f"\nERRO! São necessários pelo menos {minimo} registros (há {len(dados)})."
        )
        print("Gere dados simulados em: Dados e consultas > Gerar dados simulados.")
        return None
    return dados


def cadastrar_modulos():
    """Repete o cadastro enquanto o usuário quiser registrar mais módulos."""
    print("\nPor favor, preencha corretamente cada dado!")
    while True:
        modulo = inserir_dados()
        salvar_modulo(modulo)
        outro = input("\nDeseja cadastrar outro módulo? (s/n): ").strip().lower()
        if outro != "s":
            print("Cadastro encerrado.")
            return


if __name__ == "__main__":
    print("OLÁ! Seja bem-vindo(a) ao Registro Manual de Dados!")
    cadastrar_modulos()
