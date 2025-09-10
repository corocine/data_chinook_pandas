# Análise de Vendas da Loja de Músicas Chinook

Este projeto consiste em um dashboard interativo desenvolvido com Streamlit para a análise de dados de vendas da Chinook, uma loja de músicas digital fictícia. O dashboard oferece visualizações sobre a receita, clientes, gêneros musicais mais populares e desempenho dos funcionários.

## Tecnologias Utilizadas

- **Python:** Linguagem principal do projeto.
- **Streamlit:** Framework utilizado para a criação do dashboard web interativo.
- **Pandas:** Biblioteca para manipulação e análise de dados.
- **Plotly:** Biblioteca para a criação de gráficos interativos.
- **SQLite:** Banco de dados relacional que armazena os dados brutos da Chinook.
- **Parquet:** Formato de arquivo colunar utilizado para armazenar os dados processados, otimizando a leitura e o armazenamento.

## Arquitetura do Projeto

O projeto é estruturado para separar a preparação dos dados da aplicação principal, garantindo melhor desempenho e manutenibilidade.

### Fluxo de Dados

1. **Dados Brutos:** Os dados originais residem em um banco de dados SQLite (`data/chinook.db`).
2. **Script de Preparação:** O script `src/scripts/build_parquet.py` executa uma consulta SQL complexa para unir tabelas (invoices, customers, tracks, etc.), realiza transformações básicas com Pandas e salva o resultado consolidado no formato Parquet (`data/chinook_processed.parquet`).
3. **Dashboard:** A aplicação Streamlit (`src/main.py`) carrega o arquivo Parquet pré-processado, o que é significativamente mais rápido do que consultar o banco de dados diretamente a cada interação do usuário. O dashboard então renderiza as métricas e visualizações.

### Estrutura de Diretórios

```

.

├── data/

│   ├── chinook.db              # Banco de dados original

│   └── chinook_processed.parquet # Dados processados

├── src/

│   ├── components/             # Módulos reutilizáveis da UI (gráficos, filtros)

│   ├── scripts/

│   │   └── build_parquet.py    # Script para processar os dados

│   └── main.py                 # Ponto de entrada da aplicação Streamlit

├── notebooks/                  # Jupyter notebooks para exploração de dados

├── requirements.txt            # Dependências do projeto

└── README.md                   # Documentação do projeto

```

## Como Iniciar o Projeto

Siga os passos abaixo para executar o dashboard localmente.

### Pré-requisitos

- Python 3.8 ou superior
- Git

### Passos

1. **Clone o repositório:**

   ```bash

   git clone <URL_DO_REPOSITORIO_AQUI>

   cd <NOME_DO_DIRETORIO_DO_PROJETO>

   ```
2. **Crie e ative um ambiente virtual:**

   ```bash

   # Para Windows

   python -m venv venv

   venv\Scripts\activate


   # Para macOS/Linux

   python3 -m venv venv

   source venv/bin/activate

   ```
3. **Instale as dependências:**

   ```bash

   pip install -r requirements.txt

   ```
4. **Processe os dados:**

   Execute o script para criar o arquivo Parquet a partir do banco de dados SQLite.

   ```bash

   python src/scripts/build_parquet.py

   ```
5. **Execute a aplicação Streamlit:**

   ```bash

   streamlit run src/main.py

   ```

   A aplicação estará disponível em seu navegador no endereço `http://localhost:8501`.
