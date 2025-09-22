import os
import subprocess
from scripts.bronze_ingest import get_matches, save_bronze
from scripts.silver_transform import transform_bronze_to_silver
from scripts.gold_metrics import generate_team_metrics

# Configuração da competição
COMPETITION = "BSA"  # Brasileirão Série A

def run_pipeline():
    print("🚀 Iniciando pipeline de dados do Brasileirão...")

    # 1. Bronze: buscar dados da API
    print("\n📥 Etapa 1: Ingestão (Bronze)")
    matches = get_matches(competition=COMPETITION, season=2025)
    save_bronze(matches, competition=COMPETITION)

    # 2. Silver: transformar em tabela limpa
    print("\n⚙️ Etapa 2: Transformação (Silver)")
    df_silver = transform_bronze_to_silver(competition=COMPETITION)
    print(df_silver.head())

    # 3. Gold: calcular métricas finais
    print("\n🏆 Etapa 3: Métricas (Gold)")
    df_gold = generate_team_metrics(competition=COMPETITION)
    print(df_gold.head())

    # 4. Dashboard: rodar com Streamlit
    print("\n📊 Etapa 4: Dashboard (abrindo no navegador)")
    subprocess.run(["streamlit", "run", "dashboard/app.py"])

if __name__ == "__main__":
    run_pipeline()
