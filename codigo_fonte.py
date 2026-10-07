# Estrutura do Projeto
# modulos/: Leitura, cadastro e consulta de dados em CSV.
# simulacao/: Geração de dados simulados da colônia.
# calculos/: Indicadores, tratamento de erros, modelos, Grid/Random Search, método de Euler, eletricidade e gráficos.
# alertas/: Priorização de alertas utilizando Heap.
# busca/: Busca por prefixo utilizando Trie.
# relatorio/: Resumo da análise final.
# menus/: Interface dos menus do terminal.

from menus.menu_dados import menu_dados
from menus.menu_alertas import menu_alertas
from menus.menu_sistemas import menu_sistemas
from menus.menu_analises import menu_analises
from menus.menu_analise_final import menu_analise_final
from menus.menu_glossario import menu_glossario
from menus.menu_repetir import repetir


def main():
    # Mostra o menu principal e chama o submenu escolhido, até o usuário sair
    while True:
        print("\n==========================================")
        print("          SCIC - AURORA SIGER")
        print(" Sistema de Comunicação Interplanetária")
        print("==========================================")
        print("Muito bem-vindo(a) ao nosso sistema! Que ação gostaria de tomar?\n")
        print("1 - Dados e consultas")
        print("2 - Análises e previsão")
        print("3 - Alertas e buscas")
        print("4 - Sistemas e eletricidade")
        print("5 - Análise final (gera o resumo da colônia)")
        print("6 - Glossário (o que é cada informação)")
        print("0 - Sair\n")
        opcao = input("Digite uma opção de 0 a 6:\n-->")

        match opcao:
            case "1":
                menu_dados()
            case "2":
                menu_analises()
            case "3":
                menu_alertas()
            case "4":
                menu_sistemas()
            case "5":
                menu_analise_final()
            case "6":
                menu_glossario()
            case "0":
                print("\nEncerrando o SCIC...")
                print("Sistema finalizado.")
                break
            case _:
                print("\nOpção inválida. Tente novamente.")
                continue

        # depois de cada ação, pergunta se o usuário quer continuar
        if repetir() == 2:
            print("\nEncerrando o SCIC...")
            print("Sistema finalizado.")
            break


# so roda o menu quando este arquivo é executado diretamente (e não quando é importado)
if __name__ == "__main__":
    main()
