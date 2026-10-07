"""Pergunta, depois de cada ação, se o usuário quer continuar usando o sistema."""


def repetir():
    """Devolve 1 (continuar) ou 2 (encerrar). Repete a pergunta se a resposta for inválida."""
    while True:
        print(
            "Deseja consultar mais alguma informação ou realizar mais alguma ação?\n"
            "1 - Sim\n"
            "2 - Não (encerrar app)"
        )
        try:
            resposta = int(input("\nDigite a opção desejada: "))
            if resposta < 1 or resposta > 2:
                print("ERRO DETECTADO! A opção deve ser 1 ou 2!\nPor favor, tente novamente\n")
                continue
            return resposta
        except ValueError:
            # int() falhou: o usuário digitou letra ou deixou vazio
            print("ERRO DETECTADO! A opção deve ser um número inteiro!\nTente novamente\n")
