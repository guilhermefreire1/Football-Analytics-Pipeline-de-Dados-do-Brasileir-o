# ⚽ Football Analytics – Pipeline de Dados do Brasileirão

Este projeto implementa um **pipeline de Engenharia de Dados em camadas (Bronze → Silver → Gold)** utilizando a [Football Data API](https://www.football-data.org/), com foco no **Campeonato Brasileiro (BSA – Série A)**.  

O pipeline coleta dados de partidas, trata e transforma em métricas de desempenho, e disponibiliza tudo em um **dashboard interativo** via [Streamlit](https://streamlit.io/).

---

## 📂 Estrutura do Projeto

football-analytics/
│── config/ # Configurações do projeto
│ ├── init.py
│ └── settings.py # API Key e URL base
│
│── data/ # Camadas do pipeline
│ ├── bronze/ # Dados crus (JSON da API)
│ ├── silver/ # Dados tratados (CSV tabular)
│ └── gold/ # Métricas finais (classificação dos times)
│
│── dashboard/ # Dashboard em Streamlit
│ └── app.py
│
│── scripts/ # Scripts ETL
│ ├── bronze_ingest.py # Coleta da API → Bronze
│ ├── silver_transform.py # JSON bruto → CSV tabular (Silver)
│ ├── gold_metrics.py # KPIs e métricas finais (Gold)
│
│── run_pipeline.py # Executa Bronze + Silver + Gold + Dashboard
│── requirements.txt # Dependências
│── README.md # Documentação


---

## 🔑 Configuração da API

1. Crie uma conta gratuita em [Football Data](https://www.football-data.org/).  
2. Copie sua **API Key**.  
3. No arquivo `config/settings.py`, coloque sua chave:

```python
API_KEY = "SUA_CHAVE_AQUI"
BASE_URL = "https://api.football-data.org/v4"

## ⚙️ Instalação

git clone https://github.com/seuusuario/football-analytics.git
cd football-analytics

# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

## 🚀 Executando o Pipeline Completo

python run_pipeline.py

Isso vai:

Baixar dados da API (camada Bronze)

Transformar em CSV tabular (camada Silver)

Calcular classificação, pontos, saldo de gols e aproveitamento (camada Gold)

Abrir o dashboard no navegador (http://localhost:8501)

## Autor

Projeto desenvolvido por Guilherme Henrique como estudo prático de Engenharia de Dados aplicada ao futebol.