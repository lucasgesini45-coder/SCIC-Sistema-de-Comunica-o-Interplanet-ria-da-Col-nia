# SCIC — Sistema de Comunicação Interplanetária da Colônia

Sistema desenvolvido em **Python** para monitoramento, consulta e análise dos sistemas da colônia espacial **Aurora Siger**.

O **SCIC (Sistema de Comunicação Interplanetária da Colônia)** foi desenvolvido como uma aplicação de terminal capaz de centralizar informações dos módulos da colônia, analisar indicadores de comunicação e utilizar um modelo de **Machine Learning** para realizar previsões relacionadas à latência dos sistemas.

---

# 1. Sobre o Projeto

A colônia **Aurora Siger** possui diferentes módulos responsáveis por funções essenciais, como comunicação, habitação, agricultura, laboratório, suporte médico, armazenamento, energia e controle.

O SCIC foi desenvolvido para auxiliar no monitoramento desses módulos por meio de uma interface de terminal organizada em menus e submenus.

O sistema utiliza uma base de dados em formato **CSV**, permitindo consultar informações dos módulos e realizar análises sobre o comportamento dos sistemas de comunicação.

Além da análise dos dados, o projeto incorpora um modelo de **Regressão Linear** para realizar previsões da latência observada.

---

# 2. Objetivo

O principal objetivo do SCIC é desenvolver uma solução capaz de:

* Centralizar informações dos módulos da colônia;
* Permitir consultas aos registros disponíveis;
* Monitorar indicadores de comunicação;
* Identificar diferenças entre latência prevista e observada;
* Classificar situações de erro;
* Identificar módulos com maior impacto;
* Utilizar Machine Learning para realizar previsões;
* Organizar o sistema de forma modular e expansível.

---

# 3. Cenário da Aurora Siger

A **Aurora Siger** representa uma colônia interplanetária composta por diferentes sistemas responsáveis pela manutenção e operação da infraestrutura.

Cada módulo possui informações relacionadas à sua operação, incluindo:

* Latência prevista;
* Latência observada;
* Tensão;
* Corrente;
* Status;
* Prioridade;
* Código do sensor;
* Mensagens operacionais;
* Ciclo de operação.

Essas informações são utilizadas pelo SCIC para realizar consultas e análises.

---

# 4. Funcionalidades

## 4.1 Dados e Consultas

O sistema permite:

* Visualizar os dados completos da colônia;
* Consultar módulos específicos;
* Realizar buscas pelo nome do módulo;
* Exibir os registros encontrados.

A consulta utiliza o nome informado pelo usuário e realiza a busca sem diferenciação entre letras maiúsculas e minúsculas.

---

## 4.2 Análise de Indicadores

O sistema calcula indicadores relacionados à comunicação dos módulos.

São calculados:

**Erro absoluto:**

```text
Erro absoluto = |Latência observada - Latência prevista|
```

**Erro relativo:**

```text
Erro relativo = (Erro absoluto / Latência prevista) × 100
```

A partir desses valores, cada registro é classificado de acordo com a gravidade do erro.

### Classificação

| Erro relativo        | Situação |
| -------------------- | -------- |
| Menor que 10%        | Normal   |
| Entre 10% e 25%      | Atenção  |
| Maior ou igual a 25% | Crítico  |

O sistema também identifica:

* Média do erro absoluto;
* Média do erro relativo;
* Maior erro absoluto;
* Módulo com maior erro;
* Quantidade de registros classificados como Normal;
* Quantidade de registros classificados como Atenção;
* Quantidade de registros classificados como Crítico.

---

# 5. Machine Learning e Previsão

Uma das principais funcionalidades do projeto é a utilização de **Machine Learning** para realizar previsões relacionadas à latência dos módulos.

O modelo utilizado é uma **Regressão Linear**, disponibilizada pela biblioteca Scikit-learn.

As variáveis utilizadas como entrada do modelo são:

```text
latencia_prevista
tensao
corrente
```

O valor utilizado como variável de saída é:

```text
latencia_observada
```

O conjunto de dados é dividido em duas partes:

```text
Dados
  │
  ├── 80% → Treinamento
  │
  └── 20% → Teste
```

A divisão utiliza `train_test_split`, com `random_state=42`, garantindo reprodutibilidade da separação dos dados.

Após o treinamento, o modelo realiza previsões sobre os registros destinados ao conjunto de teste.

Os resultados são apresentados comparando:

```text
Latência Real
        ×
Latência Prevista pelo Modelo
```

---

# 6. Base de Dados

Os dados utilizados pelo sistema estão armazenados no arquivo:

```text
dados_aurora_siger.csv
```

A base contém registros referentes aos diferentes módulos da colônia.

### Principais campos

| Campo                | Descrição                 |
| -------------------- | ------------------------- |
| `id`                 | Identificador do registro |
| `modulo`             | Nome do módulo            |
| `tipo`               | Categoria do módulo       |
| `latencia_prevista`  | Latência esperada         |
| `latencia_observada` | Latência registrada       |
| `tensao`             | Tensão elétrica           |
| `corrente`           | Corrente elétrica         |
| `status`             | Situação atual do módulo  |
| `prioridade`         | Nível de prioridade       |
| `codigo_sensor`      | Identificação do sensor   |
| `mensagem`           | Mensagem operacional      |
| `ciclo`              | Ciclo de operação         |

A base contém registros de diferentes áreas da colônia, como comunicação, habitação, agricultura, laboratório, suporte médico, armazenamento, controle e energia.

---

# 7. Estrutura do Sistema

O sistema foi organizado de forma modular, separando as responsabilidades entre diferentes arquivos.

```text
SCIC/
│
├── codigo_fonte.py
├── dados_aurora_siger.csv
├── README.md
│
└── modulos/
    ├── __init__.py
    ├── alertas.py
    ├── analises.py
    ├── buscas.py
    ├── dados.py
    └── sistemas.py
```

### `codigo_fonte.py`

Responsável pelo funcionamento principal da aplicação.

Contém:

* Menu principal;
* Submenu de dados;
* Submenu de análises;
* Submenu de alertas;
* Submenu de sistemas;
* Análise final;
* Controle de navegação do usuário.

---

### `modulos/dados.py`

Responsável pelo acesso e consulta dos dados.

Principais funções:

```python
visualizar_dados()
consultar_modulo()
```

Utiliza **Pandas** para carregar e manipular o arquivo CSV.

---

### `modulos/analises.py`

Responsável pelas análises e pelo modelo de previsão.

Principais funções:

```python
calcular_indicadores()
executar_modelo_previsao()
```

Utiliza:

* Pandas;
* Scikit-learn;
* Regressão Linear;
* Train/Test Split.

---

### Módulos adicionais

O projeto também possui módulos estruturados para futuras funcionalidades:

```text
alertas.py
buscas.py
sistemas.py
```

Esses módulos fazem parte da arquitetura planejada para expansão do sistema.

---

# 8. Menu Principal

Ao executar o programa, o usuário encontra o menu principal:

```text
==========================================
          SCIC - AURORA SIGER
 Sistema de Comunicação Interplanetária
==========================================

1 - Dados e consultas
2 - Análises e previsão
3 - Alertas e buscas
4 - Sistemas e eletricidade
5 - Análise final
0 - Sair

========================================
```

Cada opção direciona o usuário para um submenu específico.

---

# 9. Tratamento de Erros

O sistema utiliza estruturas de tratamento de exceções com `try/except` para evitar que erros internos interrompam a execução da aplicação de forma inesperada.

Entre os casos tratados estão:

* Arquivo de dados não encontrado;
* Colunas necessárias ausentes no CSV;
* Erros durante o cálculo dos indicadores;
* Erros durante a execução do modelo de previsão.

Quando ocorre um problema, o sistema apresenta uma mensagem orientando o usuário sobre o possível motivo do erro.

Exemplo:

```text
Não foi possível executar a previsão.

Algumas informações necessárias ainda
não foram calculadas.

Execute primeiro:

2 - Análises e previsão
1 - Calcular indicadores e erros
```

Essa abordagem melhora a experiência de utilização e evita a apresentação de mensagens técnicas extensas diretamente ao usuário.

---

# 10. Tecnologias Utilizadas

As principais tecnologias utilizadas no desenvolvimento são:

```text
Python
Pandas
Scikit-learn
Linear Regression
CSV
Git
GitHub
```

### Python

Utilizado como linguagem principal para desenvolvimento da aplicação.

### Pandas

Utilizado para leitura, manipulação e análise dos dados armazenados no CSV.

### Scikit-learn

Utilizado para implementação do modelo de Machine Learning.

### Linear Regression

Utilizada para realizar previsões relacionadas à latência observada dos módulos.

### Git e GitHub

Utilizados para controle de versão, armazenamento e gerenciamento do código-fonte.

---

# 11. Como Executar

## Pré-requisitos

É necessário possuir o **Python** instalado no computador.

Também é necessário instalar as bibliotecas utilizadas pelo projeto:

```bash
pip install pandas scikit-learn
```

## Execução

Clone o repositório:

```bash
git clone https://github.com/lucasgesini45-coder/SCIC-Sistema-de-Comunica-o-Interplanet-ria-da-Col-nia.git
```

Acesse a pasta:

```bash
cd SCIC-Sistema-de-Comunica-o-Interplanet-ria-da-Col-nia
```

Execute o sistema:

```bash
python codigo_fonte.py
```

---

# 12. Fluxo de Funcionamento

O funcionamento geral do sistema pode ser representado da seguinte forma:

```text
             ┌──────────────────┐
             │    Usuário       │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │  Menu Principal  │
             └────────┬─────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       Dados       Análises    Alertas
          │           │
          ▼           ▼
        CSV       Indicadores
                      │
                      ▼
               Machine Learning
                      │
                      ▼
                 Previsões
```

---

# 13. Organização do Desenvolvimento

O projeto foi desenvolvido de forma modular, permitindo separar as responsabilidades entre diferentes arquivos e facilitar futuras expansões.

A separação dos módulos permite que novas funcionalidades sejam adicionadas sem concentrar toda a lógica em um único arquivo.

A estrutura também facilita a manutenção e a compreensão do código.

---

# 14. Limitações e Evolução

O projeto possui funcionalidades estruturadas para futuras etapas de desenvolvimento.

Entre as possibilidades de evolução estão:

* Implementação da priorização de alertas utilizando **Heap**;
* Implementação de buscas utilizando **Trie**;
* Desenvolvimento dos recursos de sistemas e eletricidade;
* Implementação da avaliação detalhada do modelo de previsão;
* Ampliação das análises estatísticas;
* Inclusão de novos modelos de Machine Learning;
* Criação de uma interface gráfica ou web;
* Persistência dos dados em banco de dados;
* Implementação de novos mecanismos de monitoramento.

Essas possibilidades permitem que o SCIC evolua de uma aplicação de terminal para uma plataforma mais completa de monitoramento e análise.

---

# 15. Integrantes da Equipe

| Integrante                         | RM       |
| ---------------------------------- | -------- |
| Lucas Ribeiro Gesini               | RM569383 |
| Calebe Gonçalves Garcia de Souza   | RM568743 |
| Filipe Souza Nascimento            | RM573758 |
| Rafael De Freitas Silva            | RM570089 |
| Paulo Henrique Gonçalves Bueno     | RM570456 |

---

# 16. Projeto Acadêmico

O **SCIC — Sistema de Comunicação Interplanetária da Colônia** foi desenvolvido como projeto acadêmico, aplicando conceitos de programação, análise de dados, estruturas modulares e Inteligência Artificial.

O projeto integra diferentes conhecimentos de desenvolvimento de software para representar uma solução de monitoramento aplicada a um cenário de exploração e colonização interplanetária.

---

# 17. Repositório

O código-fonte e a documentação do projeto estão disponíveis no GitHub:

**SCIC — Sistema de Comunicação Interplanetária da Colônia**

https://github.com/lucasgesini45-coder/SCIC-Sistema-de-Comunica-o-Interplanet-ria-da-Col-nia

---

# 18. Considerações Finais

O SCIC demonstra a aplicação prática de conceitos de **Python, análise de dados e Machine Learning** em um sistema organizado por módulos.

A combinação entre processamento dos dados, cálculo de indicadores e utilização de um modelo de Regressão Linear permite que o sistema não apenas consulte informações da colônia, mas também realize análises e previsões sobre o comportamento dos módulos.

O projeto estabelece uma base para futuras evoluções, permitindo incorporar novas técnicas de análise, estruturas de dados e recursos de monitoramento à medida que o sistema for expandido.
