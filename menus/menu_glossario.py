"""
Glossário do SCIC: explica cada informação cadastrada para os módulos da Aurora Siger.
Pode ser aberto pelo menu principal (main.py) ou executado com: python -m menus.menu_glossario
"""

import textwrap

# O glossário é um dicionário: cada GRUPO (chave) guarda uma lista de itens.
# Cada item é uma dupla (título, explicação). Para incluir um termo novo, basta acrescentar uma dupla.
GRUPOS = {
    "Identificação do módulo": [
        (
            "Nome e tipo do módulo",
            "A Aurora Siger é dividida em módulos, cada um com uma função: habitação, "
            "agricultura, comunicação, laboratório, suporte médico e armazenamento de "
            "dados. O tipo ajuda a decidir a importância: um módulo de suporte médico "
            "ou de comunicação costuma exigir resposta mais rápida que um de armazenamento.",
        ),
        (
            "Código do dispositivo/sensor",
            "É o identificador do sensor ou medidor instalado no módulo, como SEN-A1F. "
            "Os computadores guardam esse tipo de código em outras bases numéricas. "
            "Exemplo: a parte A1F, em hexadecimal, vale 2591 em decimal e 1010 0001 1111 "
            "em binário. Esse código também serve para buscas por prefixo (trie).",
        ),
        (
            "Ciclo de registro",
            "É o número da leitura em que os dados foram coletados (ciclo 1, 2, 3...). "
            "Com vários ciclos é possível acompanhar a evolução de um módulo e perceber "
            "se um problema foi pontual ou se está se repetindo.",
        ),
    ],
    "Comunicação": [
        (
            "Latência observada (ms)",
            "É o tempo real, em milissegundos, que uma mensagem leva para ir de um ponto "
            "a outro e ser confirmada. Quanto maior, mais lenta é a comunicação. Na "
            "comunicação interplanetária ela já é naturalmente alta, por isso o importante "
            "é compará-la com o valor esperado.",
        ),
        (
            "Latência prevista (ms)",
            "É o valor que o sistema esperava para aquele módulo, estimado por um modelo "
            "simples de previsão. Serve de referência: se a observada fica muito acima da "
            "prevista, algo pode estar errado no enlace de comunicação.",
        ),
        (
            "Erro absoluto",
            "É a diferença, sem sinal, entre a latência observada e a prevista:\n"
            "erro absoluto = |observada - prevista|.\n"
            "Exemplo: observada 320,5 ms e prevista 300 ms dão erro de 20,5 ms.",
        ),
        (
            "Erro relativo (%)",
            "Compara o erro absoluto com o valor previsto:\n"
            "erro relativo = erro absoluto / prevista x 100.\n"
            "Como é uma porcentagem, permite comparar módulos com escalas diferentes: "
            "20 ms de erro pesa muito num enlace de 100 ms, mas pouco num de 5000 ms. "
            "O sistema considera acima de 10% como fora do limite aceitável.",
        ),
    ],
    "Eletricidade": [
        (
            "Tensão (V)",
            "É a 'força' que empurra a corrente elétrica pelo circuito, medida em volts. "
            "Na Aurora Siger, representa a tensão de alimentação do equipamento do módulo, "
            "como um transmissor de rádio. Tensão fora da faixa de operação pode indicar "
            "falha na fonte de energia ou risco de danos ao equipamento.",
        ),
        (
            "Corrente (A)",
            "É a quantidade de carga elétrica que passa pelo circuito a cada segundo, "
            "medida em ampères. Uma corrente acima do normal pode indicar sobrecarga ou "
            "defeito, e abaixo do normal pode indicar mau contato ou equipamento parado.",
        ),
        (
            "Potência (W)",
            "É a energia usada por segundo pelo equipamento: P = V x I. O sistema calcula "
            "esse valor sozinho. Exemplo: 24 V x 2,5 A = 60 W. Na comunicação, ajuda a "
            "estimar a potência de um transmissor e a controlar o consumo de energia "
            "da colônia.",
        ),
        (
            "Lei de Ohm (apoio)",
            "Relaciona tensão, corrente e resistência: V = R x I. Com os dados do "
            "cadastro dá para estimar a resistência do circuito. Exemplo: 24 V e 2,5 A "
            "indicam R = 24 / 2,5 = 9,6 ohms.",
        ),
    ],
    "Situação e prioridade": [
        (
            "Status do módulo",
            "Mostra em que situação o módulo está:\n"
            "- Ativo: operando dentro do limite aceitável.\n"
            "- Atenção: próximo do limite, merece acompanhamento.\n"
            "- Alerta: fora do limite, exige ação.\n"
            "- Manutenção: desligado ou em reparo programado.\n"
            "- Inativo: sem comunicação.",
        ),
        (
            "Prioridade do módulo (1 a 5)",
            "Indica a importância do módulo para a colônia: 1 é baixa e 5 é alta. É um "
            "dos critérios que o sistema usa para ordenar os alertas na fila de "
            "prioridade (heap), para que o mais urgente seja tratado primeiro.",
        ),
        (
            "Persistência",
            "É o número de ciclos seguidos em que o módulo ficou fora do limite. Um "
            "pico isolado costuma ser passageiro, mas vários ciclos seguidos indicam "
            "um problema real. Serve de critério de desempate na fila de alertas.",
        ),
        (
            "Mensagem do alerta",
            "É um texto curto que descreve o problema, como 'latência acima do "
            "previsto'. Ele aparece na análise final e facilita a decisão da equipe.",
        ),
    ],
    "Conceitos do sistema": [
        (
            "Fila de prioridade (heap)",
            "Estrutura de dados que mantém sempre o item mais importante no topo. "
            "Diferente de uma lista simples, que precisaria ser reordenada ou percorrida "
            "inteira a cada novo alerta, o heap encontra o mais urgente rapidamente.",
        ),
        (
            "Trie (busca por prefixo)",
            "Árvore em que cada nó é uma letra e palavras com o mesmo começo dividem o "
            "mesmo caminho. Para achar tudo que começa com 'com', o sistema desce três "
            "nós e coleta o que está abaixo, sem comparar com todos os termos.",
        ),
        (
            "Modelo de previsão e treino/teste",
            "Regressão linear que estima a latência a partir do tipo do módulo, da "
            "potência e do ciclo. Os dados são divididos em treino (o modelo aprende) e "
            "teste (o modelo é avaliado em dados que nunca viu), com MAE, MSE, RMSE e R².",
        ),
        (
            "Validação, Grid Search e Random Search",
            "Os dados são divididos em treino (o modelo aprende), validação (serve para "
            "escolher o melhor modelo) e teste (nota final, guardada até o fim). Grid Search "
            "testa todas as combinações de parâmetros de uma grade; Random Search sorteia só "
            "algumas, o que é mais rápido mas pode perder a melhor.",
        ),
        (
            "Método de Euler",
            "Método numérico que calcula uma grandeza que muda no tempo em pequenos passos de "
            "tamanho h. Aqui simula a latência voltando ao normal depois de um pico. É uma "
            "aproximação: quanto menor o passo, menor o erro, mas mais contas são feitas.",
        ),
        (
            "Ponto flutuante e arredondamento",
            "O computador guarda decimais em binário, então muitos valores são aproximados "
            "(0,1 + 0,2 dá 0,30000000000000004). Esses erros são minúsculos perto dos limites "
            "de decisão da colônia, mas é por isso que se compara com tolerância e não com ==.",
        ),
        (
            "Gerenciamento inteligente da comunicação",
            "Sensores medem os módulos continuamente, o sistema compara o previsto com o "
            "observado, e alertas são priorizados automaticamente. Mas a decisão final "
            "continua sendo da equipe humana, que valida o que o sistema sugere.",
        ),
    ],
}


def mostrar_item(titulo, texto):
    """Mostra um item do glossário com o texto quebrado em linhas de 60 caracteres."""
    print("\n" + "=" * 60)
    print(titulo.upper())
    print("=" * 60)
    for paragrafo in texto.split("\n"):
        print(
            textwrap.fill(
                paragrafo,
                width=60,
                subsequent_indent="  " if paragrafo.startswith("-") else "",
            )
        )


def ler_opcao(maximo):
    """Lê um número de 0 até maximo, repetindo a pergunta se vier algo inválido."""
    while True:
        try:
            n = int(input("--> "))
            if 0 <= n <= maximo:
                return n
            print(f"ERRO! Digite um número de 0 a {maximo}.")
        except ValueError:
            print("ERRO! O valor deve ser um número inteiro.")


def menu_glossario():
    """Lista todos os itens numerados e mostra a explicação do que o usuário escolher."""
    itens = [item for grupo in GRUPOS.values() for item in grupo]
    while True:
        print("\n--- Glossário: o que é cada informação? ---")
        n = 1
        for grupo, lista in GRUPOS.items():
            print(f"\n[{grupo}]")
            for titulo, _ in lista:
                print(f"{n:2}. {titulo}")
                n += 1
        print("\n 0. Voltar ao menu principal")
        opcao = ler_opcao(len(itens))
        if opcao == 0:
            return
        mostrar_item(*itens[opcao - 1])
        input("\nPressione Enter para voltar à lista...")


if __name__ == "__main__":
    menu_glossario()
