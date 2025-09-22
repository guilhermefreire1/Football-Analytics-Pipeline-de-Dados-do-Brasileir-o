import os                      # Usado para manipular pastas e arquivos
import pandas as pd            # Usado para trabalhar com tabelas (DataFrame)
from datetime import datetime  # Usado para lidar com datas (nome de arquivos, etc.)

# Função que gera as métricas da camada Gold
def generate_team_metrics(competition="BSA"):
    print("🚀 Iniciando geração de métricas...")  # Mensagem de início

    # Garante que a pasta "data/gold" existe (se não existir, cria)
    os.makedirs("data/gold", exist_ok=True)

    # Caminho da pasta Silver (onde estão os CSVs transformados)
    silver_path = "data/silver"

    # Lista todos os arquivos da pasta Silver que começam com "matches_{competition}"
    # Exemplo: matches_PL_2025-09-21.csv
    files = [f for f in os.listdir(silver_path) if f.startswith(f"matches_{competition}")]
    print(f"📂 Arquivos encontrados em {silver_path}: {files}")

    # Se não encontrar nenhum arquivo, mostra aviso e encerra
    if not files:
        print("❌ Nenhum arquivo encontrado no Silver para essa competição.")
        return

    # Ordena a lista de arquivos encontrados e pega o mais recente
    latest_file = sorted(files)[-1]
    file_path = os.path.join(silver_path, latest_file)
    print(f"📂 Usando arquivo: {file_path}")

    # Lê o CSV da camada Silver em um DataFrame
    df = pd.read_csv(file_path)
    print(f"📊 Linhas lidas do Silver: {len(df)}")

    # Dicionário que vai guardar estatísticas de cada time
    stats = {}

    # Percorre cada linha (partida) do DataFrame
    for _, row in df.iterrows():
        home = row["home_team"]      # Nome do time mandante
        away = row["away_team"]      # Nome do time visitante
        gh = row["score_home"]       # Gols do mandante
        ga = row["score_away"]       # Gols do visitante

        # Se o jogo não tem placar (ainda não jogado), pula
        if pd.isna(gh) or pd.isna(ga):
            continue

        # Inicializa os dois times no dicionário, caso ainda não existam
        for team in [home, away]:
            if team not in stats:
                stats[team] = {
                    "points": 0,        # Pontos
                    "wins": 0,          # Vitórias
                    "draws": 0,         # Empates
                    "losses": 0,        # Derrotas
                    "goals_for": 0,     # Gols a favor
                    "goals_against": 0  # Gols contra
                }

        # Atualiza gols marcados e sofridos
        stats[home]["goals_for"] += gh
        stats[home]["goals_against"] += ga
        stats[away]["goals_for"] += ga
        stats[away]["goals_against"] += gh

        # Define o resultado da partida
        if gh > ga:  # Vitória do mandante
            stats[home]["points"] += 3
            stats[home]["wins"] += 1
            stats[away]["losses"] += 1
        elif gh < ga:  # Vitória do visitante
            stats[away]["points"] += 3
            stats[away]["wins"] += 1
            stats[home]["losses"] += 1
        else:  # Empate
            stats[home]["points"] += 1
            stats[away]["points"] += 1
            stats[home]["draws"] += 1
            stats[away]["draws"] += 1

    # Se nenhum jogo teve placar registrado, avisa e encerra
    if not stats:
        print("⚠️ Nenhum jogo com placar encontrado (todos podem estar agendados).")
        return

    # Converte o dicionário "stats" em um DataFrame
    df_stats = pd.DataFrame.from_dict(stats, orient="index").reset_index()
    df_stats.rename(columns={"index": "team"}, inplace=True)  # Renomeia a coluna para "team"

    # Calcula saldo de gols
    df_stats["goal_difference"] = df_stats["goals_for"] - df_stats["goals_against"]

    # Calcula o número total de partidas disputadas
    df_stats["matches_played"] = df_stats["wins"] + df_stats["draws"] + df_stats["losses"]

    # Calcula a taxa de vitórias (percentual de jogos vencidos)
    df_stats["win_rate_%"] = (df_stats["wins"] / df_stats["matches_played"] * 100).round(2)

    # Ordena a tabela por pontos (desc) e saldo de gols (desc), simulando uma classificação oficial
    df_stats = df_stats.sort_values(by=["points", "goal_difference"], ascending=[False, False])

    # Gera o caminho do arquivo de saída (Camada Gold)
    today = datetime.today().strftime("%Y-%m-%d")
    gold_path = f"data/gold/team_performance_{competition}_{today}.csv"

    # Salva a tabela em CSV
    df_stats.to_csv(gold_path, index=False, encoding="utf-8")

    print(f"✅ Métricas salvas em {gold_path}")
    print(df_stats.head())  # Mostra as 5 primeiras linhas no terminal

    return df_stats

# Executa a função se rodar o script diretamente
if __name__ == "__main__":
    competition = "BSA" 
    generate_team_metrics(competition)
