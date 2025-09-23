# ---------------------------------------------------------------
# Importações de bibliotecas necessárias
# ---------------------------------------------------------------
import os                  # Para manipulação de diretórios e arquivos
import json                # Para abrir e manipular arquivos JSON salvos na camada Bronze
import pandas as pd        # Para transformar os dados em tabelas (DataFrames)
from datetime import datetime  # Para lidar com datas (nomear arquivos, converter colunas)

# ---------------------------------------------------------------
# Função principal que transforma os arquivos Bronze → Silver
# ---------------------------------------------------------------
def transform_bronze_to_silver(competition="BSA"):
    """
    Lê os arquivos de partidas da camada Bronze (JSON),
    transforma em dados tabulares (CSV) e salva na camada Silver.
    competition: código da competição (ex: 'BSA' = Brasileirão Série A)
    """

    # Garante que a pasta data/silver exista (se não existir, cria automaticamente)
    os.makedirs("data/silver", exist_ok=True)

    # Define a pasta da camada Bronze
    bronze_path = "data/bronze"

    # Lista todos os arquivos do diretório Bronze que começam com "matches_{competition}"
    files = [f for f in os.listdir(bronze_path) if f.startswith(f"matches_{competition}")]

    # Se não houver nenhum arquivo correspondente, lança um erro
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado em {bronze_path} para {competition}")

    # Pega o arquivo mais recente (último da lista ordenada por nome)
    latest_file = sorted(files)[-1]

    # Monta o caminho completo do arquivo dentro da pasta Bronze
    file_path = os.path.join(bronze_path, latest_file)

    print(f"📂 Usando arquivo: {file_path}")

    # Abre o arquivo JSON da camada Bronze em modo leitura
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extrai a lista de partidas do JSON (chave "matches")
    matches = data.get("matches", [])

    # Lista que armazenará os dicionários com dados de cada partida
    rows = []

    # Itera sobre todas as partidas retornadas no JSON
    for m in matches:
        # Para cada partida, cria um dicionário com as informações principais
        rows.append({
            "match_id": m.get("id"),   # ID único da partida
            "utc_date": m.get("utcDate"),   # Data da partida (formato UTC)
            "status": m.get("status"),      # Status da partida (SCHEDULED, FINISHED, etc.)
            "competition": m["competition"]["name"] if m.get("competition") else competition,  # Nome da competição
            "season_start": m["season"]["startDate"] if m.get("season") else None,  # Início da temporada
            "season_end": m["season"]["endDate"] if m.get("season") else None,      # Fim da temporada
            "home_team": m["homeTeam"]["name"] if m.get("homeTeam") else None,     # Nome do time da casa
            "away_team": m["awayTeam"]["name"] if m.get("awayTeam") else None,     # Nome do time visitante
            "score_home": m["score"]["fullTime"]["home"] if m.get("score") else None,  # Gols do time da casa
            "score_away": m["score"]["fullTime"]["away"] if m.get("score") else None   # Gols do time visitante
        })

    # Converte a lista de dicionários em um DataFrame do Pandas
    df = pd.DataFrame(rows)

    # Converte a coluna "utc_date" para o tipo datetime do Pandas
    # Isso permite ordenar e manipular datas facilmente
    df["utc_date"] = pd.to_datetime(df["utc_date"])

    # Gera o nome do arquivo de saída baseado na data atual
    today = datetime.today().strftime("%Y-%m-%d")
    silver_path = f"data/silver/matches_{competition}_{today}.csv"

    # Salva o DataFrame em CSV dentro da camada Silver
    df.to_csv(silver_path, index=False, encoding="utf-8")

    # Mensagem de sucesso exibida no console
    print(f"✅ Dados transformados e salvos em {silver_path}")

    # Retorna o DataFrame para uso posterior (ex: camada Gold)
    return df

# ---------------------------------------------------------------
# Bloco principal (executado apenas se rodar este arquivo direto)
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Define a competição como Brasileirão Série A (BSA)
    competition = "BSA"
    
    # Executa a função para transformar Bronze → Silver
    transform_bronze_to_silver(competition)
