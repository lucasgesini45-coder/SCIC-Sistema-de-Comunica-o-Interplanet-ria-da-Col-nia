# Roteiro — execução e explicação do SCIC

Este trecho complementa a introdução e os slides já gravados. Duração sugerida: 4 a 6 minutos, sem limite obrigatório conhecido. As amostras visuais dos slides mostram Heap, Trie e sistemas como próximas etapas; por isso a versão revisada mantém esse escopo. A gravação de tela enviada tem cerca de 1min36s e não possui faixa de áudio. Confira se pretende narrá-la antes de unir os vídeos. A introdução tem cerca de 19s e possui áudio; este roteiro não depende da transcrição dessa fala.

## Antes de gravar

- Extraia o ZIP e abra a pasta SCIC no VS Code.
- Siga o README para criar o ambiente e instalar as dependências antes da gravação.
- Selecione o interpretador `.venv` no VS Code.
- Deixe abertos `codigo_fonte.py`, `modulos/dados.py` e `modulos/analises.py`.
- Amplie a fonte do editor e do terminal. Use a tela inteira para mostrar as tabelas.
- No Mac, abra a gravação com `Shift + Command + 5`. Nas opções, selecione o microfone e faça um teste curto para confirmar a voz.
- Se usar F5, digite no terminal integrado. Não use um painel de saída que não aceite `input()`.

## Parte 1 — mostrar o programa funcionando (aproximadamente 2min30s)

### 1. Início

**Na tela:** terminal na pasta SCIC. Execute:

```bash
python codigo_fonte.py
```

**Fala:**

“Agora vou demonstrar o SCIC em execução no VS Code. O programa funciona pelo terminal, com menus que permitem consultar os dados da colônia e analisar a latência da comunicação.”

### 2. Visualizar os dados

**Digite:** `1` no menu principal; depois `1` no submenu.

**Fala:**

“Nesta opção, o sistema lê os dados do arquivo CSV e apresenta a tabela. A base tem trinta registros: dez módulos observados em três ciclos. Cada registro inclui latência prevista e observada, tensão, corrente, status e prioridade.”

Mostre o cabeçalho e algumas linhas, sem ler toda a tabela.

### 3. Consultar um módulo

**Digite:** `2`; quando solicitado, `Laboratorio`.

**Fala:**

“Também podemos consultar um módulo específico. Ao informar parte do nome, o sistema apresenta os registros correspondentes. Neste exemplo, aparecem as três observações do Laboratório Orion. A consulta não diferencia letras maiúsculas e minúsculas.”

**Digite:** `0` para voltar ao menu principal.

### 4. Calcular indicadores

**Digite:** `2` no menu principal; depois `1` no submenu.

**Fala:**

“O sistema calcula o erro absoluto, que é a diferença em módulo entre a latência observada e a prevista. Depois calcula o erro relativo, dividindo essa diferença pela latência prevista e multiplicando por cem.”

“Por exemplo, no primeiro ciclo do Habitat Alpha, a latência prevista é de cento e cinquenta milissegundos e a observada é de duzentos e dez. O erro absoluto é sessenta milissegundos e o relativo é quarenta por cento, classificado como crítico.”

“O resumo apresenta as médias, o maior erro e a quantidade de registros em cada classificação. Erros abaixo de dez por cento são normais; de dez até menos de vinte e cinco por cento indicam atenção; a partir de vinte e cinco por cento são críticos.”

### 5. Executar o modelo

**Digite:** `2` no submenu de análises.

**Fala:**

“Nesta etapa, usamos regressão linear para estimar a latência observada. O modelo recebe três entradas: latência prevista, tensão e corrente. A base é dividida em vinte e quatro registros para treinamento e seis para teste. A tabela compara a previsão do modelo com o valor real dos registros de teste.”

### 6. Avaliar o desempenho

**Digite:** `3` no submenu de análises.

**Fala:**

“Aqui avaliamos o erro médio absoluto nos mesmos registros de teste. Na base fornecida, o erro da estimativa original é aproximadamente trinta e nove vírgula sessenta e sete milissegundos. O erro do modelo é dezoito vírgula trinta e cinco, uma redução de cerca de cinquenta e três vírgula sete por cento.”

“O R quadrado é aproximadamente zero vírgula cinquenta e três. Ele é uma medida de ajuste, não uma porcentagem de acertos. Como a base é pequena e repete módulos em diferentes ciclos, esse resultado é exploratório. Precisamos de mais dados e validação temporal para avaliar a previsão de ciclos futuros.”

**Digite:** `0` para voltar; depois `0` para sair.

## Parte 2 — explicar o código (aproximadamente 2 minutos)

### 7. Arquivo principal: `codigo_fonte.py`

**Mostre:** imports, função `menu_analises`, função `main` e bloco final `if __name__ == "__main__"`.

**Fala:**

“O arquivo principal organiza a interface. As funções dos módulos são importadas no início, enquanto os menus ficam neste arquivo. O laço while mantém o programa em execução e o match case direciona cada opção para a função correspondente. A opção zero volta ao menu anterior ou encerra o sistema.”

“A função executar análise trata erros de dados e informa o problema no terminal. O bloco final chama a função main somente quando este arquivo é executado diretamente. Isso evita iniciar o menu ao importar o arquivo.”

### 8. Dados: `modulos/dados.py`

**Mostre:** `CAMINHO_CSV`, `carregar_dados` e `consultar_modulo`.

**Fala:**

“Neste módulo, o Pandas carrega o CSV em uma tabela chamada DataFrame. O caminho é calculado a partir da localização do projeto, evitando depender da pasta em que o terminal foi aberto.”

“A função carregar dados verifica as colunas obrigatórias e valida os valores. A base é carregada uma vez e compartilhada com as análises. A função consultar módulo filtra a coluna de nomes usando o texto informado pelo usuário. A busca é literal, então caracteres digitados não são interpretados como expressões regulares.”

### 9. Análises: `modulos/analises.py`

**Mostre:** `classificar_erro`, cálculos em `calcular_indicadores`, `treinar_modelo` e `avaliar_desempenho`.

**Fala:**

“A função calcular indicadores utiliza operações sobre as colunas para obter os erros e aplicar a classificação. Quando a latência prevista é zero, o erro relativo é marcado como indefinido, evitando divisão por zero.”

“Na função treinar modelo, X contém as variáveis de entrada e y contém a latência observada. A função train test split separa treino e teste. O random state igual a quarenta e dois torna essa divisão reproduzível. O fit ajusta os coeficientes da regressão nos dados de treino, e o predict calcula as previsões nos dados de teste.”

“Na avaliação, calculamos o erro médio absoluto e o R quadrado. A comparação com a previsão original utiliza os mesmos registros de teste, para que os dois resultados sejam comparáveis.”

### 10. Encerramento

**Mostre:** arquivos reservados `alertas.py`, `buscas.py` e `sistemas.py` no explorador.

**Fala:**

“O projeto separa a navegação, os dados e as análises em módulos, facilitando a manutenção. Como foi apresentado nos slides, Heap, Trie e os recursos de sistemas permanecem planejados para as próximas etapas. Nesta versão, demonstramos as consultas, os indicadores e a regressão linear funcionando.”

## Sequência de teclas para ensaiar

Cada item corresponde a uma entrada seguida de Enter:

| Entrada | Resultado |
| --- | --- |
| 1 | Dados e consultas |
| 1 | Tabela completa |
| 2 | Consulta de módulo |
| Laboratorio | Registros do Laboratório Orion |
| 0 | Menu principal |
| 2 | Análises e previsão |
| 1 | Indicadores |
| 2 | Previsões |
| 3 | Avaliação |
| 0 | Menu principal |
| 0 | Encerramento |

## Pontos para não confundir na fala

- “Previsão original” é a coluna `latencia_prevista`; “previsão do modelo” é calculada pela regressão.
- O teste usa seis registros, não toda a base.
- O modelo treina novamente com a mesma divisão quando solicitado; não aprende continuamente.
- R² de 0,53 não significa 53% de acertos.
- O CSV é uma base simulada; o programa não monitora sensores em tempo real.
- Os indicadores são calculados em memória; o CSV original não é alterado.
- Não demonstre os menus futuros como funcionalidades concluídas.
