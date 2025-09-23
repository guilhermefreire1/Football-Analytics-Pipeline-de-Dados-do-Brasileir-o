# Football Analytics – Pipeline de Dados do Brasileirão

Este projeto é um estudo prático de Engenharia de Dados aplicada ao futebol, com foco no Campeonato Brasileiro (Série A – BSA).
Ele implementa um pipeline em camadas (Bronze → Silver → Gold), coleta dados da Football Data API, trata e transforma em métricas de desempenho, e apresenta tudo em um dashboard interativo com Streamlit.

-------------------------------------------------------------------------------

CONFIGURAÇÃO DA API

1. Crie uma conta gratuita em https://www.football-data.org/
2. Copie sua API Key.
3. No arquivo config/settings.py, adicione sua chave:

API_KEY = "SUA_CHAVE_AQUI"
BASE_URL = "https://api.football-data.org/v4"

-------------------------------------------------------------------------------

INSTALAÇÃO

Clone este repositório e instale as dependências:

git clone https://github.com/guilhermefreire1/Football-Analytics-Pipeline-de-Dados-do-Brasileir-o.git
cd Football-Analytics-Pipeline-de-Dados-do-Brasileir-o

# Criar ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

Principais dependências:
- requests → Coleta de dados da API
- pandas → Transformações de dados
- streamlit → Dashboard interativo

-------------------------------------------------------------------------------

EXECUTANDO O PIPELINE COMPLETO

Execute todo o fluxo (Bronze → Silver → Gold → Dashboard) com:

python run_pipeline.py

Isso vai:
1. Baixar dados da API (camada Bronze)
2. Tratar e salvar em CSV (camada Silver)
3. Calcular classificação e métricas (camada Gold)
4. Abrir o dashboard no navegador em http://localhost:8501

-------------------------------------------------------------------------------

DASHBOARD

O dashboard exibe:
- Classificação completa do Brasileirão
- Gráfico de pontos por time
- Saldo de gols por time
- Taxa de vitórias (%)

FUTURAS MELHORIAS

- Adicionar evolução rodada a rodada (gráficos de linha)
- Ranking de artilheiros e assistências
- Deploy do dashboard em Streamlit Cloud
- Orquestração com Airflow ou Prefect
- Persistência histórica em banco de dados (PostgreSQL ou SQLite)

-------------------------------------------------------------------------------

ARQUITETURA DA PIPELINE

          ┌───────────────┐
          │   Football    │
          │   Data API    │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │   Bronze      │
          │ (JSON cru)    │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │   Silver      │
          │ (CSV limpo)   │
          └───────┬───────┘
                  │
                  ▼
        ┌──────────────────────┐
        │        Gold          │
        │  - Classificação     │
        │  - KPIs dos times    │
        │  - Artilheiros       │
        └─────────┬────────────┘
                  │
                  ▼
          ┌───────────────┐
          │   Dashboard   │
          │ (Streamlit)   │
          └───────────────┘


AUTOR

Projeto desenvolvido por Guilherme Henrique
Estudante de Sistemas de Informação | Data Engineering Enthusiast
LinkedIn: https://www.linkedin.com/in/guilhermefreire1
GitHub: https://github.com/guilhermefreire1
