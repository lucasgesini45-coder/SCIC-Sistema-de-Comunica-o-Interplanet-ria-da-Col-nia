"""
Priorização de alertas com HEAP (fila de prioridade).

Ideia: um heap é uma árvore guardada dentro de uma lista, onde o "pai" é sempre
mais urgente que os "filhos". Assim, o alerta mais urgente fica sempre na
posição 0, pronto para ser retirado sem precisar ordenar a lista inteira.

Na lista, o filho de uma posição i fica nas posições 2i+1 (esquerda) e 2i+2 (direita).
"""

import random
import time

from modulos.inserir_dados import carregar_csv

# Só entram na fila os registros com um destes status
STATUS_QUE_VIRAM_ALERTA = ("Alerta", "Atenção")


class FilaPrioridade:
    """Heap mínimo: o item com a MENOR chave é o mais urgente e fica no topo."""

    def __init__(self):
        self.itens = []  # cada item é uma dupla (chave, alerta)
        self.trocas = 0  # só para mostrar quanto trabalho o heap teve

    def __len__(self):
        return len(self.itens)

    def _vem_antes(self, posicao_a, posicao_b):
        """True se o item da posição A é mais urgente (chave menor) que o da posição B."""
        return self.itens[posicao_a][0] < self.itens[posicao_b][0]

    def _trocar(self, posicao_a, posicao_b):
        self.itens[posicao_a], self.itens[posicao_b] = self.itens[posicao_b], self.itens[posicao_a]
        self.trocas += 1

    def _subir(self, posicao):
        """heapify-up: o item novo sobe enquanto for mais urgente que o pai."""
        while posicao > 0:
            pai = (posicao - 1) // 2
            if self._vem_antes(posicao, pai):
                self._trocar(posicao, pai)
                posicao = pai
            else:
                break  # já está no lugar certo

    def _descer(self, posicao):
        """heapify-down: o item desce enquanto algum filho for mais urgente que ele."""
        quantidade = len(self.itens)
        while True:
            filho_esquerdo = 2 * posicao + 1
            filho_direito = 2 * posicao + 2
            mais_urgente = posicao

            # Descobre quem é o mais urgente entre o item e seus dois filhos
            if filho_esquerdo < quantidade and self._vem_antes(filho_esquerdo, mais_urgente):
                mais_urgente = filho_esquerdo
            if filho_direito < quantidade and self._vem_antes(filho_direito, mais_urgente):
                mais_urgente = filho_direito

            if mais_urgente == posicao:
                break  # nenhum filho é mais urgente: terminou
            self._trocar(posicao, mais_urgente)
            posicao = mais_urgente

    def inserir(self, chave, alerta):
        """Coloca o alerta no fim da lista e deixa ele subir até o lugar certo."""
        self.itens.append((chave, alerta))
        self._subir(len(self.itens) - 1)

    def topo(self):
        """Olha o mais urgente sem retirar."""
        return self.itens[0][1] if self.itens else None

    def remover_topo(self):
        """Retira e devolve o mais urgente. O último item vai para a raiz e desce."""
        if not self.itens:
            return None
        primeiro = self.itens[0]
        ultimo = self.itens.pop()
        if self.itens:
            self.itens[0] = ultimo
            self._descer(0)
        return primeiro[1]


def chave_alerta(alerta, ordem_no_arquivo):
    """
    Define a "nota de urgência" de um alerta. Como o heap é mínimo, usamos
    valores negativos: quanto MAIOR a prioridade, MENOR (e mais urgente) a chave.
    Critérios, em ordem: prioridade do módulo > persistência > erro relativo.
    O último número só desempata alertas totalmente iguais.
    """
    return (
        -alerta["prioridade"],
        -alerta["persistencia"],
        -alerta["erro_relativo_pct"],
        ordem_no_arquivo,
    )


def montar_fila(dados):
    """Percorre os dados e coloca no heap cada registro que está em Alerta ou Atenção."""
    fila = FilaPrioridade()
    for ordem, registro in enumerate(dados.to_dict("records")):
        if registro["status"] in STATUS_QUE_VIRAM_ALERTA:
            fila.inserir(chave_alerta(registro, ordem), registro)
    return fila


def top_alertas(dados, quantos=5):
    """Devolve os 'quantos' alertas mais urgentes, do mais para o menos urgente."""
    fila = montar_fila(dados)
    resultado = []
    while len(fila) and len(resultado) < quantos:
        resultado.append(fila.remover_topo())
    return resultado


# ------------------------------------------------------------
# Telas do menu
# ------------------------------------------------------------
def mostrar_ranking(lista):
    """Imprime os alertas em forma de tabela."""
    print(f"\n{'Pos':<4}{'Código':<9}{'Módulo':<25}{'Status':<9}{'Prio':<5}{'Pers':<5}{'Erro%':<8}Mensagem")
    print("-" * 95)
    for posicao, alerta in enumerate(lista, 1):
        print(
            f"{posicao:<4}{alerta['codigo_sensor']:<9}{str(alerta['nome'])[:23]:<25}{alerta['status']:<9}"
            f"{alerta['prioridade']:<5}{alerta['persistencia']:<5}{alerta['erro_relativo_pct']:<8.2f}"
            f"{alerta['mensagem_alerta']}"
        )


def ver_ranking():
    """Mostra os 10 alertas mais urgentes, na ordem em que o heap os entrega."""
    dados = carregar_csv()
    if dados is None:
        return
    fila = montar_fila(dados)
    total = len(fila)
    if total == 0:
        print("\nNenhum registro com status Alerta ou Atenção. Nada para priorizar.")
        return

    print(f"\n{total} alerta(s) na fila (status Alerta ou Atenção).")
    print("Critério: maior prioridade do módulo > maior persistência > maior erro relativo.")

    ranking = []
    while len(fila) and len(ranking) < 10:
        ranking.append(fila.remover_topo())
    mostrar_ranking(ranking)
    if total > 10:
        print(f"\n(mostrando os 10 mais urgentes de {total})")

    mais_urgente = ranking[0]
    print(
        f"\nAlerta mais urgente: {mais_urgente['nome']} ({mais_urgente['codigo_sensor']}) "
        f"- {mais_urgente['mensagem_alerta']}."
    )


def ver_estrutura():
    """Mostra como os alertas ficam guardados dentro do heap (a lista e os níveis da árvore)."""
    dados = carregar_csv()
    if dados is None:
        return
    fila = montar_fila(dados)
    if len(fila) == 0:
        print("\nNenhum alerta para montar o heap.")
        return

    print(f"\nHeap com {len(fila)} alerta(s) guardado em uma lista (vetor):")
    for posicao, (_, alerta) in enumerate(fila.itens[:15]):
        pai = "raiz" if posicao == 0 else f"pai = posição {(posicao - 1) // 2}"
        print(
            f"  [{posicao:>2}] {alerta['codigo_sensor']:<8} prio {alerta['prioridade']}  "
            f"pers {alerta['persistencia']}  erro {alerta['erro_relativo_pct']:>6.2f}%   ({pai})"
        )
    if len(fila) > 15:
        print(f"  ... e mais {len(fila) - 15} posições")

    # Mostra a árvore por níveis: nível 0 tem 1 item, nível 1 tem 2, nível 2 tem 4...
    print("\nOs 3 primeiros níveis da árvore (o topo é o mais urgente):")
    inicio, largura, nivel = 0, 1, 0
    while inicio < len(fila) and nivel < 3:
        codigos = [
            fila.itens[j][1]["codigo_sensor"]
            for j in range(inicio, min(inicio + largura, len(fila)))
        ]
        print(f"  nível {nivel}: " + "   ".join(codigos))
        inicio += largura
        largura *= 2
        nivel += 1
    print(f"\nPara montar o heap foram feitas {fila.trocas} troca(s) de posição (heapify-up).")


def comparar_com_lista(quantidade=2000):
    """Compara o tempo do heap com o de uma lista simples, usando alertas aleatórios."""
    print(f"\nTeste com {quantidade} alertas aleatórios: retirar todos, do mais urgente ao menos urgente.")
    sorteio = random.Random(42)
    chaves = [
        (-sorteio.randint(1, 5), -sorteio.randint(0, 10), -sorteio.uniform(10, 200), i)
        for i in range(quantidade)
    ]

    # Com heap: inserir tudo e ir retirando o topo
    inicio = time.perf_counter()
    fila = FilaPrioridade()
    for chave in chaves:
        fila.inserir(chave, chave)
    while len(fila):
        fila.remover_topo()
    tempo_heap = time.perf_counter() - inicio

    # Com lista simples: a cada retirada, percorre tudo para achar o menor
    inicio = time.perf_counter()
    lista = list(chaves)
    while lista:
        menor = min(lista)
        lista.remove(menor)
    tempo_lista = time.perf_counter() - inicio

    print(f"  Heap:          {tempo_heap * 1000:8.1f} ms")
    print(f"  Lista simples: {tempo_lista * 1000:8.1f} ms")
    if tempo_heap > 0:
        print(f"  A lista simples foi cerca de {tempo_lista / tempo_heap:.1f}x mais lenta.")
    print("Os tempos variam de computador para computador, mas a diferença cresce com o nº de alertas.")


def explicar():
    """Texto explicativo pedido no enunciado (representação, critério, vantagem)."""
    print("""
================ COMO O HEAP PRIORIZA OS ALERTAS ================
1) Como os alertas são representados
   Cada registro com status Alerta ou Atenção vira um dicionário com
   módulo, código do sensor, prioridade, persistência, erro relativo e mensagem.

2) Critério de prioridade
   Maior prioridade do módulo (1 a 5); empate: maior persistência (ciclos
   seguidos fora do limite); empate: maior erro relativo.

3) Como o heap organiza os alertas
   É uma árvore guardada em uma lista: o filho de i fica em 2i+1 e 2i+2.
   Regra: o pai é sempre mais urgente que os filhos, então o topo é o mais urgente.
   Ao inserir, o alerta sobe (heapify-up). Ao retirar o topo, o último
   alerta vai para a raiz e desce (heapify-down).

4) Como o sistema escolhe o alerta mais urgente
   Basta olhar a posição 0 do heap, sem percorrer a lista.

5) Vantagem sobre uma lista simples
   Lista: achar o mais urgente exige percorrer tudo (O(n)) ou reordenar a
   lista a cada novo alerta. Heap: inserir e retirar custam O(log n).
   Com muitos alertas chegando em tempo real, isso faz diferença.
=================================================================""")


def menu_heap():
    """Submenu da priorização de alertas."""
    while True:
        print("\n========================================")
        print("      PRIORIZAÇÃO DE ALERTAS (HEAP)")
        print("========================================")
        print("1 - Ver ranking dos alertas")
        print("2 - Ver como o heap organiza os alertas")
        print("3 - Comparar heap com lista simples")
        print("4 - Entender o critério e a vantagem")
        print("0 - Voltar")
        opcao = input("Digite uma opção: ").strip()
        if opcao == "1":
            ver_ranking()
        elif opcao == "2":
            ver_estrutura()
        elif opcao == "3":
            comparar_com_lista()
        elif opcao == "4":
            explicar()
        elif opcao == "0":
            return
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_heap()
