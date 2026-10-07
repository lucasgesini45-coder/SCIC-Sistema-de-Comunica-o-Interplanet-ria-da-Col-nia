"""
Busca por prefixo com TRIE.

Uma trie é uma árvore em que cada nó representa uma letra. Palavras que começam
igual compartilham o mesmo caminho. Para achar tudo que começa com "com", basta
descer pelos nós c -> o -> m e coletar o que está abaixo, sem comparar o
prefixo com todas as palavras cadastradas.
"""

import unicodedata

from modulos.inserir_dados import carregar_csv, ler_inteiro, ler_texto


def normalizar(texto):
    """Deixa tudo em minúsculas e sem acento: 'Comunicação' e 'comunicacao' viram o mesmo caminho."""
    separado = unicodedata.normalize("NFD", str(texto).lower().strip())
    # Remove só os acentos (caracteres da categoria "Mn" = marcas de acento)
    return "".join(letra for letra in separado if unicodedata.category(letra) != "Mn")


class No:
    """Um nó da trie."""

    def __init__(self):
        self.filhos = {}  # letra -> próximo nó
        self.original = None  # a palavra como foi cadastrada (só preenchido onde a palavra termina)
        self.registros = []  # linhas do CSV ligadas a essa palavra


class Trie:
    def __init__(self):
        self.raiz = No()
        self.nos = 1  # quantidade de nós (para mostrar no "como funciona")
        self.termos = 0  # quantidade de palavras diferentes guardadas

    def inserir(self, termo, registro):
        """Guarda uma palavra, criando os nós que ainda não existem no caminho."""
        chave = normalizar(termo)
        if not chave:
            return
        no = self.raiz
        for letra in chave:
            if letra not in no.filhos:
                no.filhos[letra] = No()
                self.nos += 1
            no = no.filhos[letra]
        # Chegamos ao último nó: aqui a palavra termina
        if no.original is None:
            no.original = str(termo)
            self.termos += 1
        no.registros.append(registro)

    def buscar_prefixo(self, prefixo):
        """Devolve todas as palavras que começam com o prefixo."""
        # Passo 1: desce pelo caminho do prefixo. Se faltar uma letra, não há resultados.
        no = self.raiz
        for letra in normalizar(prefixo):
            if letra not in no.filhos:
                return []
            no = no.filhos[letra]
        # Passo 2: coleta tudo que está abaixo desse nó
        resultados = []
        self._coletar(no, resultados)
        return resultados

    def _coletar(self, no, resultados):
        """Percorre a subárvore e junta as palavras encontradas (em ordem alfabética)."""
        if no.original is not None:
            resultados.append((no.original, no.registros))
        for letra in sorted(no.filhos):
            self._coletar(no.filhos[letra], resultados)


def palavras(texto):
    """Quebra um texto em palavras com 3 letras ou mais (palavras curtas não ajudam na busca)."""
    return [palavra for palavra in str(texto).replace(",", " ").split() if len(palavra) >= 3]


def construir_indices(dados):
    """Cria uma trie para módulos, outra para sensores e outra para alertas."""
    dados = dados.fillna({"mensagem_alerta": ""})  # evita que uma mensagem vazia vire a palavra 'nan'
    trie_modulos, trie_sensores, trie_alertas = Trie(), Trie(), Trie()

    for ordem, registro in enumerate(dados.to_dict("records")):
        registro["ordem"] = ordem
        # Módulos: o nome completo, o tipo e cada palavra deles
        for termo in [registro["nome"], registro["tipo"]] + palavras(registro["nome"]) + palavras(registro["tipo"]):
            trie_modulos.inserir(termo, registro)
        # Sensores: o código inteiro (ex: SEN-A1F)
        trie_sensores.inserir(registro["codigo_sensor"], registro)
        # Alertas: cada palavra da mensagem e o status
        for palavra in palavras(registro["mensagem_alerta"]) + [registro["status"]]:
            trie_alertas.inserir(palavra, registro)

    return {
        "1": ("módulos e tipos", [trie_modulos]),
        "2": ("códigos de sensores", [trie_sensores]),
        "3": ("palavras-chave de alertas", [trie_alertas]),
        "4": ("todos", [trie_modulos, trie_sensores, trie_alertas]),
    }


def buscar():
    """Pergunta onde e o que buscar, e mostra os termos e os registros mais recentes."""
    dados = carregar_csv()
    if dados is None:
        return
    indices = construir_indices(dados)

    print("\nOnde buscar?")
    print("1. Módulos e tipos (ex: com -> Comunicação)")
    print("2. Códigos de sensores (ex: SEN-A -> SEN-A1F)")
    print("3. Palavras-chave de alertas (ex: lat -> Latência)")
    print("4. Em tudo")
    escolha = str(ler_inteiro("--> ", 1, 4))
    descricao, tries = indices[escolha]

    prefixo = ler_texto("Digite o prefixo: ")
    achados = []
    for trie in tries:
        achados += trie.buscar_prefixo(prefixo)

    if not achados:
        print(f"\nNenhum resultado em {descricao} para o prefixo '{prefixo}'.")
        return

    print(f"\n{len(achados)} termo(s) encontrado(s) em {descricao} começando com '{prefixo}':")
    for termo, registros in achados[:15]:
        print(f"  - {termo}  ({len(registros)} registro(s))")
    if len(achados) > 15:
        print(f"  ... e mais {len(achados) - 15} termo(s)")

    # Junta os registros sem repetir (o mesmo registro pode aparecer em vários termos)
    unicos = {registro["ordem"]: registro for _, registros in achados for registro in registros}
    recentes = sorted(unicos.values(), key=lambda r: (-r["ciclo"], r["ordem"]))[:10]

    print(f"\nRegistros mais recentes ({len(recentes)} de {len(unicos)}):")
    print(f"{'Ciclo':<6}{'Código':<9}{'Módulo':<25}{'Status':<11}{'Obs(ms)':<9}Mensagem")
    print("-" * 85)
    for registro in recentes:
        print(
            f"{registro['ciclo']:<6}{registro['codigo_sensor']:<9}{str(registro['nome'])[:23]:<25}"
            f"{registro['status']:<11}{registro['latencia_observada']:<9.1f}{registro['mensagem_alerta']}"
        )


def explicar():
    """Explica por que a trie é boa para busca por prefixo, com números reais dos dados."""
    dados = carregar_csv()
    print("""
================ COMO A TRIE FUNCIONA ================
- Cada nó guarda uma letra; palavras com o mesmo começo dividem o mesmo
  caminho. Ex: "comunicação" e "comando" compartilham c -> o -> m.
- Buscar o prefixo "com": descer c -> o -> m (3 passos) e coletar tudo
  que está abaixo desse nó.
- Por que é adequada: o custo da busca depende do tamanho do prefixo, e
  não de quantos termos existem. Numa lista, seria preciso comparar o
  prefixo com todos os termos, um por um.
- Aqui ela indexa nomes de módulos, códigos de sensores e palavras-chave
  de alertas, ignorando maiúsculas e acentos.""")
    if dados is not None:
        indices = construir_indices(dados)
        for _, (descricao, tries) in indices.items():
            if len(tries) == 1:  # a opção "todos" tem 3 tries, então é pulada
                trie = tries[0]
                print(f"  Índice de {descricao}: {trie.termos} termo(s) em {trie.nos} nó(s).")
    print("======================================================")


def menu_trie():
    """Submenu da busca por prefixo."""
    while True:
        print("\n========================================")
        print("        BUSCA POR PREFIXO (TRIE)")
        print("========================================")
        print("1 - Buscar por prefixo")
        print("2 - Como a trie funciona")
        print("0 - Voltar")
        opcao = input("Digite uma opção: ").strip()
        if opcao == "1":
            buscar()
        elif opcao == "2":
            explicar()
        elif opcao == "0":
            return
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_trie()
