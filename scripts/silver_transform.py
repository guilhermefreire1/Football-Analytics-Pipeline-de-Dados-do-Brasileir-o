import os          # Para manipular pastas e arquivos
import json        # Para abrir os arquivos JSON salvos no Bronze
import pandas as pd  # Para transformar os dados em tabelas (DataFrame)
from datetime import datetime  # Para trabalhar com datas (nome de arquivos e conversão)

# Função que pega os arquivos crus (Bronze) e transforma em dados tabulares (Silver)
def transform_bronze_to_silver(competition="BSA"):

    # Garante que a pasta data/silver existe (se não existir, cria)
    os.makedirs("data/silver", exist_ok=True)

    # Pega todos os arquivos da pasta bronze que começam com "matches_{competition}"
    bronze_path = "data/bronze"
    files = [f for f in os.listdir(bronze_path) if f.startswith(f"matches_{competition}")]

    # Se não tiver nenhum arquivo correspondente, gera erro
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado em {bronze_path} para {competition}")

    # Pega o arquivo mais recente (último da lista ordenada)
    latest_file = sorted(files)[-1]
    file_path = os.path.join(bronze_path, latest_file)

    print(f"📂 Usando arquivo: {file_path}")

    # Abre o arquivo JSON (camada Bronze)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    #Normaliza os dados das partidas
    matches = data.get("matches", [])
    rows = []  # Lista que vai guardar os dicionários (cada linha do CSV)
    for m in matches:
        rows.append({
            "match_id": m.get("id"),
            "utc_date": m.get("utcDate"),
            "status": m.get("status"),
            "competition": m["competition"]["name"] if m.get("competition") else competition,
            "season_start": m["season"]["startDate"] if m.get("season") else None,
            "season_end": m["season"]["endDate"] if m.get("season") else None,
            "home_team": m["homeTeam"]["name"] if m.get("homeTeam") else None,
            "away_team": m["awayTeam"]["name"] if m.get("awayTeam") else None,
            "score_home": m["score"]["fullTime"]["home"] if m.get("score") else None,
            "score_away": m["score"]["fullTime"]["away"] if m.get("score") else None
        })

    # Converte a lista de dicionários em um DataFrame do Pandas (tabela)
    df = pd.DataFrame(rows)

     # Converte a coluna de datas (utc_date) para o tipo datetime do Pandas
    df["utc_date"] = pd.to_datetime(df["utc_date"])

    # Gera um nome de arquivo baseado na data de hoje
    today = datetime.today().strftime("%Y-%m-%d")
    silver_path = f"data/silver/matches_{competition}_{today}.csv"

    # Salva o DataFrame em CSV dentro da camada Silver
    df.to_csv(silver_path, index=False, encoding="utf-8")

    print(f"✅ Dados transformados e salvos em {silver_path}")
    return df

if __name__ == "__main__":
    competition = "BSA"  # pode trocar para "BSA" (Brasileirão) ou outra
    transform_bronze_to_silver(competition)
