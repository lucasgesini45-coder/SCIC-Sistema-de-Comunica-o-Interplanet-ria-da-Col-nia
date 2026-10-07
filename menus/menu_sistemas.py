"""Submenu 4: dispositivos, bases numéricas, eletricidade e gerenciamento inteligente."""

from calculos.sistemas import (
    menu_dispositivos,
    menu_bases,
    menu_potencia,
    gerenciamento_inteligente,
)


def menu_sistemas():
    while True:
        print("\n========================================")
        print("      SISTEMAS E ELETRICIDADE")
        print("========================================\n")
        print("1 - Dispositivos de entrada e saída")
        print("2 - Conversão de bases numéricas")
        print("3 - Cálculo de potência")
        print("4 - Gerenciamento inteligente")
        print("0 - Voltar")
        print("========================================\n")
        opcao = input("Digite uma opção de 0 a 4:\n-->")

        match opcao:
            case "1":
                menu_dispositivos()
            case "2":
                menu_bases()
            case "3":
                menu_potencia()
            case "4":
                gerenciamento_inteligente()
            case "0":
                break
            case _:
                print("\nOpção inválida. Tente novamente.")
