# ---------------------------------------------------------------
# Importação de bibliotecas e funções do projeto
# ---------------------------------------------------------------
import os                      # Biblioteca padrão, útil para lidar com diretórios (não está sendo usada diretamente aqui)
import subprocess              # Usado para executar comandos externos, como abrir o Streamlit no navegador

# Importa as funções responsáveis pelas diferentes camadas do pipeline
from scripts.bronze_ingest import get_matches, save_bronze        # Camada Bronze → coleta dados da API e salva como JSON
from scripts.silver_transform import transform_bronze_to_silver   # Camada Silver → transforma JSON em CSV tabular
from scripts.gold_metrics import generate_team_metrics            # Camada Gold → gera métricas de desempenho dos times
from scripts.scorers_ingest import get_scorers                    # Camada Gold extra → gera ranking de artilheiros

# ---------------------------------------------------------------
# Definição da competição
# ---------------------------------------------------------------
COMPETITION = "BSA"  # Brasileirão Série A (código "BSA" na Football Data API)

# ---------------------------------------------------------------
# Função principal que executa o pipeline completo
# ---------------------------------------------------------------
def run_pipeline():
    print("🚀 Iniciando pipeline de dados do Brasileirão...")

    # ------------------------------
    # 1. Bronze → Coletar dados crus
    # ------------------------------
    print("\n📥 Etapa 1: Ingestão (Bronze)")
    # Chama a API para buscar as partidas do Brasileirão 2025
    matches = get_matches(competition=COMPETITION, season=2025)
    # Salva os dados crus (JSON) na camada Bronze
    save_bronze(matches, competition=COMPETITION)

    # ------------------------------
    # 2. Silver → Transformar dados
    # ------------------------------
    print("\n⚙️ Etapa 2: Transformação (Silver)")
    # Converte os arquivos JSON da Bronze em tabelas CSV limpas
    df_silver = transform_bronze_to_silver(competition=COMPETITION)
    # Exibe no console as primeiras linhas da tabela resultante
    print(df_silver.head())

    # ------------------------------
    # 3. Gold → Gerar métricas dos times
    # ------------------------------
    print("\n🏆 Etapa 3: Métricas (Gold)")
    # Calcula pontos, vitórias, empates, derrotas, saldo de gols, etc.
    df_gold = generate_team_metrics(competition=COMPETITION)
    # Exibe no console as primeiras linhas da classificação
    print(df_gold.head())

    # ------------------------------
    # 4. Gold extra → Ranking de artilheiros e assistências
    # ------------------------------
    print("\n🥇 Etapa 4: Ranking de Artilheiros e Assistências")
    # Busca o ranking de artilheiros (limitado aos 20 primeiros)
    df_scorers = get_scorers(competition=COMPETITION, limit=20)
    # Exibe no console os primeiros jogadores do ranking
    print(df_scorers.head())

    # ------------------------------
    # 5. Dashboard → Abrir visualização no Streamlit
    # ------------------------------
    print("\n📊 Etapa 5: Dashboard (abrindo no navegador)")
    # Executa o comando para rodar o app do Streamlit e abrir a dashboard
    subprocess.run(["streamlit", "run", "dashboard/app.py"])

# ---------------------------------------------------------------
# Bloco principal (executado apenas se rodar este arquivo direto)
# ---------------------------------------------------------------
if __name__ == "__main__":
    run_pipeline()
