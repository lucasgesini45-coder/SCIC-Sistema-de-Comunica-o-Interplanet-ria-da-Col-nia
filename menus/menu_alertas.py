"""Submenu 3: alertas (heap) e buscas (trie)."""

from alertas.alertas import menu_heap
from busca.busca import menu_trie


def menu_alertas():
    while True:
        print("\n========================================")
        print("          ALERTAS E BUSCAS")
        print("========================================\n")
        print("1 - Priorizar alertas com Heap")
        print("2 - Buscar registros com Trie")
        print("0 - Voltar")
        opcao = input("Digite uma opção de 0 a 2:\n-->")

        match opcao:
            case "1":
                menu_heap()
            case "2":
                menu_trie()
            case "0":
                break
            case _:
                print("\nOpção inválida. Tente novamente.")
