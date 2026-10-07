"""
Sistemas e eletricidade: dispositivos de entrada/saída, bases numéricas,
potência elétrica e gerenciamento inteligente da comunicação.
Sempre que possível, os exemplos partem dos dados reais do CSV.
"""

import numpy as np

from alertas.alertas import top_alertas
from modulos.inserir_dados import (
    LIMITE_ATENCAO,
    carregar_csv,
    ler_float,
    ler_inteiro,
    ler_texto,
)

DIGITOS = "0123456789ABCDEF"  # os 16 símbolos do hexadecimal
LIMITE_PERSISTENCIA = 3  # ciclos seguidos fora do limite para sugerir enlace redundante
LIMITE_TENDENCIA = 0.5  # pontos percentuais por ciclo para considerar que o erro está piorando


# ======================================================
# 1) Dispositivos de entrada e saída
# ======================================================
def menu_dispositivos():
    print("""
============ DISPOSITIVOS DE ENTRADA E SAÍDA ============
ENTRADA (alimentam o SCIC)
  - Teclado ............ cadastro manual de módulos
  - Arquivo CSV ........ leituras dos sensores simulados da colônia
  - Sensores/medidores . medem latência, tensão e corrente (simulados)
SAÍDA (mostram as informações)
  - Terminal ........... menus, tabelas, ranking de alertas e buscas
  - Arquivo de texto ... resumo da análise final (resumo_analise_final.txt)
  - Imagens PNG ........ gráficos salvos em graficos_ou_imagens/
  - Arquivo CSV ........ armazenamento dos dados gerados
INTERFACES DE COMUNICAÇÃO (apenas conceituais)
  - Rede / Wi-Fi ....... envio das leituras dos módulos até a central
  - USB ................ ligação de medidores e coleta local de dados
  - Bluetooth .......... sensores de curto alcance dentro de um módulo
=========================================================""")
    dados = carregar_csv()
    if dados is not None:
        print(
            f"Nos dados atuais: {dados['codigo_sensor'].nunique()} sensor(es) em "
            f"{dados['nome'].nunique()} módulo(s), com {len(dados)} leituras registradas."
        )


# ======================================================
# 2) Bases numéricas
# ======================================================
def decimal_para_base(numero, base):
    """
    Converte um decimal para outra base por divisões sucessivas.
    Os restos, lidos de trás para frente, formam o número na nova base.
    Devolve o texto convertido e a lista de passos (para mostrar a conta).
    """
    if numero == 0:
        return "0", []
    passos = []
    quociente = numero
    while quociente > 0:
        passos.append((quociente, quociente // base, quociente % base))
        quociente //= base
    texto = "".join(DIGITOS[resto] for _, _, resto in reversed(passos))
    return texto, passos


def expansao_posicional(texto, base):
    """Mostra o valor de cada dígito: dígito x base elevada à sua posição."""
    texto = texto.upper()
    termos = [f"{DIGITOS.index(digito)}x{base}^{posicao}" for posicao, digito in enumerate(reversed(texto))]
    return " + ".join(reversed(termos))


def agrupar_binario(binario):
    """Separa o binário em grupos de 4 bits, para ficar mais fácil de ler (1010 0001 1111)."""
    binario = binario.zfill((len(binario) + 3) // 4 * 4)  # completa com zeros à esquerda
    return " ".join(binario[i : i + 4] for i in range(0, len(binario), 4))


def mostrar_conversao(numero):
    """Mostra o número em decimal, binário e hexadecimal, com o passo a passo."""
    binario, passos_binario = decimal_para_base(numero, 2)
    hexa, passos_hexa = decimal_para_base(numero, 16)
    print(f"\n  Decimal:      {numero}")
    print(f"  Binário:      {agrupar_binario(binario)}")
    print(f"  Hexadecimal:  {hexa}")

    if numero > 0 and len(passos_binario) <= 16:
        print("\n  Decimal para binário (divisões sucessivas por 2):")
        for dividendo, quociente, resto in passos_binario:
            print(f"    {dividendo} / 2 = {quociente}, resto {resto}")
        print("  Lendo os restos de baixo para cima obtém-se o binário.")
    if numero > 0:
        print("\n  Decimal para hexadecimal (divisões por 16):")
        for dividendo, quociente, resto in passos_hexa:
            print(f"    {dividendo} / 16 = {quociente}, resto {resto} ({DIGITOS[resto]})")


def converter_numero():
    """Converte um número digitado pelo usuário (em decimal, binário ou hexadecimal)."""
    print("\nBase do número que você vai digitar:")
    print("1. Decimal\n2. Binário\n3. Hexadecimal")
    base = {1: 10, 2: 2, 3: 16}[ler_inteiro("--> ", 1, 3)]

    while True:
        texto = ler_texto("Número: ").upper().replace(" ", "")
        try:
            numero = int(texto, base)  # o Python já sabe converter de qualquer base para decimal
            if numero < 0 or len(texto) > 32:
                raise ValueError
            break
        except ValueError:
            print(f"ERRO! '{texto}' não é um número válido na base {base}.\n")

    if base != 10:
        print(f"\n  {texto} (base {base}) = {expansao_posicional(texto, base)} = {numero}")
    mostrar_conversao(numero)


def converter_codigo_sensor():
    """Pega o código de um sensor do CSV (ex: SEN-A1F) e lê a parte final como hexadecimal."""
    dados = carregar_csv()
    if dados is None:
        return
    codigos = sorted(dados["codigo_sensor"].unique())[:15]
    print("\nCódigos de sensores cadastrados:")
    for numero, codigo in enumerate(codigos, 1):
        print(f"{numero}. {codigo}")
    codigo = codigos[ler_inteiro("--> ", 1, len(codigos)) - 1]

    sufixo = codigo.split("-")[-1].upper()  # "SEN-A1F" -> "A1F"
    print(f"\nCódigo {codigo}: a parte '{sufixo}' pode ser lida como hexadecimal.")
    if all(letra in DIGITOS for letra in sufixo):
        print(f"  {sufixo} (hex) = {expansao_posicional(sufixo, 16)}")
        mostrar_conversao(int(sufixo, 16))
    else:
        print(f"  '{sufixo}' contém letras fora de 0-9 e A-F, então não é hexadecimal.")
        print("  Dica: use códigos como SEN-A1F para que o identificador possa ser convertido.")


def menu_bases():
    while True:
        print("\n========================================")
        print("      CONVERSÃO DE BASES NUMÉRICAS")
        print("========================================")
        print("1 - Converter um número (decimal, binário ou hexadecimal)")
        print("2 - Converter o código de um sensor do CSV")
        print("0 - Voltar")
        opcao = input("Digite uma opção: ").strip()
        if opcao == "1":
            converter_numero()
        elif opcao == "2":
            converter_codigo_sensor()
        elif opcao == "0":
            return
        else:
            print("\nOpção inválida. Tente novamente.")


# ======================================================
# 3) Eletricidade: potência e lei de Ohm
# ======================================================
def calcular_potencia_manual():
    """Calcula potência (P = V x I) e resistência (R = V / I) a partir de valores digitados."""
    print("\nInforme os valores medidos no equipamento (ex: transmissor de um módulo):")
    tensao = ler_float("Tensão (V): ")
    corrente = ler_float("Corrente (A): ")
    potencia = tensao * corrente
    print(f"\n  Potência P = V x I = {tensao:g} x {corrente:g} = {potencia:.2f} W ({potencia / 1000:.4f} kW)")
    if corrente > 0:  # evita dividir por zero
        print(f"  Resistência R = V / I = {tensao:g} / {corrente:g} = {tensao / corrente:.2f} ohms (lei de Ohm)")
    print(f"  Energia em 1 hora de operação: {potencia / 1000:.4f} kWh")


def potencia_dos_modulos():
    """Mostra tensão, corrente e potência médias de cada módulo, usando o CSV."""
    dados = carregar_csv()
    if dados is None:
        return
    tabela = (
        dados.groupby("nome")
        .agg(
            tensao_media=("tensao", "mean"),
            corrente_media=("corrente", "mean"),
            potencia_media=("potencia", "mean"),
        )
        .round(2)
        .sort_values("potencia_media", ascending=False)
    )
    print("\nMédias por módulo (potência = tensão x corrente):")
    print(tabela.to_string())
    total_kw = dados.groupby("nome")["potencia"].mean().sum() / 1000
    maior_consumidor = tabela.index[0]
    print(f"\nConsumo médio somado dos módulos: {total_kw:.3f} kW")
    print(f"Maior consumo médio: {maior_consumidor} ({tabela.iloc[0]['potencia_media']:.1f} W)")


def menu_potencia():
    while True:
        print("\n========================================")
        print("        CÁLCULO DE POTÊNCIA")
        print("========================================")
        print("1 - Calcular potência a partir de tensão e corrente")
        print("2 - Ver a potência dos módulos (dados do CSV)")
        print("0 - Voltar")
        opcao = input("Digite uma opção: ").strip()
        if opcao == "1":
            calcular_potencia_manual()
        elif opcao == "2":
            potencia_dos_modulos()
        elif opcao == "0":
            return
        else:
            print("\nOpção inválida. Tente novamente.")


# ======================================================
# 4) Gerenciamento inteligente da comunicação
# ======================================================
def gerenciamento_inteligente():
    """Liga cada conceito (sensores, anomalias, automação...) a um resultado real dos dados."""
    dados = carregar_csv()
    if dados is None:
        return
    print("\n====== GERENCIAMENTO INTELIGENTE DA COMUNICAÇÃO ======")

    # 1) Sensores e monitoramento contínuo
    print("\n1) Sensores e monitoramento contínuo")
    print(
        f"   {dados['codigo_sensor'].nunique()} sensores acompanham {dados['nome'].nunique()} módulos em "
        f"{dados['ciclo'].nunique()} ciclos ({len(dados)} leituras). Medir a cada ciclo permite comparar"
    )
    print("   o previsto com o observado e perceber desvios cedo.")

    # 2) Detecção de anomalias: registros com erro relativo acima do limite
    fora_do_limite = dados[dados["erro_relativo_pct"] > LIMITE_ATENCAO]
    print("\n2) Detecção de anomalias")
    print(
        f"   {len(fora_do_limite)} leitura(s) ({len(fora_do_limite) / len(dados) * 100:.1f}%) "
        f"com erro relativo acima de {LIMITE_ATENCAO:.0f}%."
    )
    if len(fora_do_limite):
        pior = fora_do_limite.loc[fora_do_limite["erro_relativo_pct"].idxmax()]
        print(
            f"   Maior desvio: {pior['nome']} ({pior['codigo_sensor']}), ciclo {int(pior['ciclo'])}, "
            f"{pior['erro_relativo_pct']:.1f}%."
        )

    # 3) Automação: o heap já escolhe o mais urgente sozinho
    print("\n3) Automação de decisões (fila de prioridade)")
    mais_urgente = top_alertas(dados, 1)
    if mais_urgente:
        alerta = mais_urgente[0]
        print(
            f"   O heap indica {alerta['nome']} ({alerta['codigo_sensor']}) como mais urgente: "
            f"{alerta['mensagem_alerta']}."
        )
        print("   A automação sugere; a equipe humana valida antes de agir.")
    else:
        print("   Nenhum alerta ativo: a automação não precisa priorizar nada agora.")

    # 4) Redundância: módulos que ficaram vários ciclos seguidos com problema
    print("\n4) Armazenamento e enlaces redundantes")
    persistencia_maxima = dados.groupby("nome")["persistencia"].max()
    persistentes = persistencia_maxima[persistencia_maxima >= LIMITE_PERSISTENCIA]
    if len(persistentes):
        for nome, ciclos in persistentes.items():
            print(f"   {nome}: ficou {int(ciclos)} ciclos seguidos fora do limite -> candidato a enlace redundante.")
    else:
        print(f"   Nenhum módulo ficou {LIMITE_PERSISTENCIA}+ ciclos seguidos fora do limite.")
    print("   Guardar o histórico em arquivo permite recuperar os dados se um enlace cair.")

    # 5) Manutenção preditiva: ajusta uma reta no erro de cada módulo.
    #    Se a reta sobe, o erro está aumentando com o tempo.
    print("\n5) Manutenção preditiva (tendência do erro relativo por ciclo)")
    piorando = []
    for nome, registros in dados.groupby("nome"):
        if registros["ciclo"].nunique() >= 3:  # precisa de alguns pontos para ter tendência
            inclinacao = np.polyfit(registros["ciclo"], registros["erro_relativo_pct"], 1)[0]
            if inclinacao > LIMITE_TENDENCIA:
                piorando.append((nome, inclinacao))
    if piorando:
        for nome, inclinacao in sorted(piorando, key=lambda item: -item[1]):
            print(f"   {nome}: erro subindo {inclinacao:.2f} pontos percentuais por ciclo -> programar manutenção.")
    else:
        print("   Nenhum módulo com tendência clara de piora.")

    # 6) Energia: quem mais consome, e por que isso importa numa microrrede
    print("\n6) Energia e microrredes")
    potencia_por_modulo = dados.groupby("nome")["potencia"].mean()
    print(
        f"   Consumo médio somado: {potencia_por_modulo.sum() / 1000:.3f} kW. "
        f"Maior consumidor: {potencia_por_modulo.idxmax()} "
        f"({potencia_por_modulo.max() / potencia_por_modulo.sum() * 100:.0f}% do total)."
    )
    print("   Numa microrrede, saber quem mais consome ajuda a dividir a energia e manter os")
    print("   módulos essenciais (comunicação e suporte médico) funcionando em caso de falta.")
    print("\n=====================================================")


if __name__ == "__main__":
    gerenciamento_inteligente()
