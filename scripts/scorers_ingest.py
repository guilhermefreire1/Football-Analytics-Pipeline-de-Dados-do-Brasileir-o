import os
import requests
import pandas as pd
from datetime import datetime
from config.settings import API_KEY, BASE_URL

def get_scorers(competition='BSA', limit=20):
    url = f"{BASE_URL}/competitions/{competition}/scorers"
    headers = { "X-Auth-Token": API_KEY}
    params = {"limit": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"⚠️ Não foi possível buscar artilheiros para {competition}. Erro {response.status_code}")
        return pd.DataFrame()  # retorna vazio ao invés de quebrar

    
    data = response.json()

    scorers = []
    for item in data.get("scorers", []):
        player = item["player"]["name"]
        team = item["team"]["name"]
        goals = item.get("goals",0)
        assists = item.get("assists", None)
        scorers.append({
            "player": player,
            "team": team,
            "goals": goals,
            "assists": assists
    
        })

    df = pd.DataFrame(scorers)

    #Salva na camada Gold
    os.makedirs("data/gold", exist_ok=True)
    today = datetime.today().strftime("%Y-%m-%d")
    file_path = f"data/gold/scorers_{competition}_{today}.csv"
    df.to_csv(file_path, index=False, encoding="utf-8")

    print(f"✅ Ranking de artilheiros salvo em {file_path}")
    return df

if __name__ == "__main__":
    df = get_scorers("BSA", limit=20)
    print(df.head())