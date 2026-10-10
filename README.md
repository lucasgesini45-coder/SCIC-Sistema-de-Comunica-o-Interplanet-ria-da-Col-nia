# SCIC — Sistema de Comunicação Interplanetária da Colônia

Aplicação acadêmica de terminal em Python para monitorar os dados simulados da colônia **Aurora Siger**. Integra consulta, análise de dados e regressão linear. Heap, Trie e sistemas permanecem planejados, conforme os slides já gravados. Não se conecta a sensores reais.

## Executar no VS Code

1. Extraia o ZIP. Abra no VS Code a pasta **SCIC**, que contém `codigo_fonte.py`.
2. Instale Python **3.10 ou superior** (recomendado: 3.11 ou 3.12) e a extensão **Python**, da Microsoft. O código usa `match/case`.
3. Abra **Terminal → Novo Terminal** e configure o ambiente:

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python codigo_fonte.py
```

**Windows / PowerShell**, usando diretamente o Python do ambiente:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe codigo_fonte.py
```

4. Para depurar, abra a paleta de comandos, escolha **Python: Select Interpreter** e selecione `.venv`. Pressione **F5**, usando a configuração **Executar SCIC**. Digite as opções no terminal integrado.

As dependências precisam ser instaladas uma vez, com internet. Depois disso, o programa usa apenas o CSV local. O caminho do CSV é calculado a partir do arquivo do módulo, portanto a execução também funciona a partir de outra pasta.

## Funcionalidades

| Menu | Recursos |
| --- | --- |
| 1 — Dados | Tabela completa e consulta por trecho literal do nome, sem diferenciar maiúsculas |
| 2 — Análises | Erros de latência, regressão linear e comparação de desempenho |
| 3 — Alertas | Estrutura de menu para próximas etapas |
| 4 — Sistemas | Estrutura de menu para próximas etapas |
| 5 — Análise final | Reservada para integração futura |

### Indicadores

- Erro absoluto: `abs(latencia_observada - latencia_prevista)`, em ms.
- Erro relativo: `erro_absoluto / latencia_prevista * 100`.
- Normal: erro menor que 10%; Atenção: de 10% até menos de 25%; Crítico: a partir de 25%.
- Quando a latência prevista é zero, o erro relativo é indefinido, fica fora da média percentual e é contado separadamente.

### Regressão linear

Entradas: `latencia_prevista`, `tensao` e `corrente`. Saída: `latencia_observada`. Divisão aleatória de 80% para treino e 20% para teste, com `random_state=42`. Na base original, são 24 registros de treino e 6 de teste.

O MAE compara o modelo com a estimativa original **nos mesmos registros de teste**. No ambiente de revisão (Pandas 2.2.3 / Scikit-learn 1.8.0), foram obtidos:

| Métrica | Resultado aproximado |
| --- | --- |
| MAE da estimativa original | 39,67 ms |
| MAE da regressão | 18,35 ms |
| Redução do MAE | 53,7% |
| R² | 0,53 |

R² não é porcentagem de acertos; pode ser negativo. Quando o MAE original é zero, não se calcula redução percentual.

**Limitações:** há somente 30 registros, com os mesmos módulos em diferentes ciclos. A divisão aleatória pode colocar registros do mesmo módulo nos dois conjuntos. Estes números não provam desempenho em ciclos futuros ou módulos novos. Para essa finalidade, ampliar a base e avaliar com separação temporal ou por módulo. O modelo não é um sistema de segurança e não garante latências positivas fora da base utilizada.

### Próximas etapas

Heap, Trie, sistemas/eletricidade e análise final integrada não estão implementados nesta entrega. Seus menus informam essa condição; os arquivos estão reservados. Essa separação mantém a versão coerente com a apresentação já gravada.

## Dados e organização

O CSV contém `id`, `modulo`, `tipo`, `latencia_prevista`, `latencia_observada`, `tensao`, `corrente`, `status`, `prioridade`, `codigo_sensor`, `mensagem` e `ciclo`.

O carregamento valida colunas obrigatórias, base não vazia, números finitos e não negativos, IDs positivos únicos, ciclos positivos, prioridade de 1 a 3 e textos preenchidos. O CSV original foi preservado. A aplicação carrega uma única base compartilhada; os indicadores calculados em memória não são gravados no CSV.

| Arquivo | Responsabilidade |
| --- | --- |
| `codigo_fonte.py` | Menus, navegação e tratamento de erros |
| `modulos/dados.py` | Leitura, validação e consultas |
| `modulos/analises.py` | Indicadores, treino e avaliação |
| `modulos/alertas.py` | Reservado para alertas futuros |
| `modulos/buscas.py` | Reservado para busca futura |
| `modulos/sistemas.py` | Reservado para sistemas futuros |
| `requirements.txt` | Dependências |
| `.vscode/launch.json` | Execução e depuração no terminal |
| `tests/test_scic.py` | Testes de regras e situações de erro |
| `ROTEIRO_GRAVACAO.md` | Falas, execução e explicação do código |

## Verificação

Na pasta SCIC, usando o Python com as dependências instaladas:

```bash
python -m unittest discover -s tests -v
```

Foram verificados os três testes automatizados e uma execução com todas as opções dos menus, além de execução a partir de outra pasta. A configuração do VS Code foi incluída; a interface do VS Code no computador do usuário não foi testada.

## Correções desta revisão

- Uma única leitura e validação do CSV para todos os módulos.
- Consulta literal: caracteres como `[` não são tratados como expressão regular.
- Proteção contra divisão por zero e avaliação com base insuficiente.
- Entrada principal protegida por `if __name__ == "__main__"`.
- Encerramento por Ctrl+C ou fim da entrada.
- Menus futuros claramente identificados, preservando o escopo dos slides gravados.
- Dependências, configuração do VS Code, testes e roteiro de apresentação.

## Integrantes

| Integrante | RM |
| --- | --- |
| Lucas Ribeiro Gesini | RM569383 |
| Calebe Gonçalves Garcia de Souza | RM568743 |
| Filipe Souza Nascimento | RM573758 |
| Raphael De Freitas Silva | RM570089 |
| Paulo Henrique Gonçalves Bueno | RM570456 |

Repositório informado na versão original: https://github.com/lucasgesini45-coder/SCIC-Sistema-de-Comunica-o-Interplanet-ria-da-Col-nia

A revisão foi feita no pacote enviado; nenhuma alteração foi publicada no repositório. Confira o enunciado da disciplina para adequar regras e escopo às exigências do professor.
