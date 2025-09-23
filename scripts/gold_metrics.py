# ---------------------------------------------------------------
# Importação de bibliotecas
# ---------------------------------------------------------------
import os                      # Usado para manipular pastas e arquivos (criar diretórios, listar arquivos, etc.)
import pandas as pd            # Usado para trabalhar com tabelas (DataFrames)
from datetime import datetime  # Usado para lidar com datas (nomear arquivos, salvar com data atual, etc.)

# ---------------------------------------------------------------
# Função que gera métricas dos times a partir da camada Silver
# ---------------------------------------------------------------
def generate_team_metrics(competition="BSA"):
    print("🚀 Iniciando geração de métricas...")  # Apenas uma mensagem de início para acompanhar no terminal

    # Garante que a pasta "data/gold" exista. Se não existir, cria automaticamente.
    os.makedirs("data/gold", exist_ok=True)

    # Define o caminho da pasta Silver (onde ficam os arquivos CSV transformados)
    silver_path = "data/silver"

    # Lista todos os arquivos da pasta Silver que começam com "matches_{competition}"
    # Exemplo: "matches_BSA_2025-09-22.csv"
    files = [f for f in os.listdir(silver_path) if f.startswith(f"matches_{competition}")]
    print(f"📂 Arquivos encontrados em {silver_path}: {files}")

    # Se não encontrar nenhum arquivo, mostra aviso e interrompe a função
    if not files:
        print("❌ Nenhum arquivo encontrado no Silver para essa competição.")
        return

    # Ordena a lista de arquivos e pega o mais recente (último da lista)
    latest_file = sorted(files)[-1]

    # Monta o caminho completo do arquivo escolhido
    file_path = os.path.join(silver_path, latest_file)
    print(f"📂 Usando arquivo: {file_path}")

    # Lê o CSV (Silver) em um DataFrame do Pandas
    df = pd.read_csv(file_path)
    print(f"📊 Linhas lidas do Silver: {len(df)}")

    # Cria um dicionário vazio que vai armazenar estatísticas de cada time
    stats = {}

    # Percorre cada linha (partida) da tabela
    for _, row in df.iterrows():
        home = row["home_team"]      # Nome do time mandante
        away = row["away_team"]      # Nome do time visitante
        gh = row["score_home"]       # Gols do time da casa
        ga = row["score_away"]       # Gols do time visitante

        # Se algum dos times não tiver placar (jogo ainda não jogado), pula essa linha
        if pd.isna(gh) or pd.isna(ga):
            continue

        # Inicializa os dois times no dicionário se ainda não existirem
        for team in [home, away]:
            if team not in stats:
                stats[team] = {
                    "points": 0,        # Pontos acumulados
                    "wins": 0,          # Vitórias
                    "draws": 0,         # Empates
                    "losses": 0,        # Derrotas
                    "goals_for": 0,     # Gols a favor
                    "goals_against": 0  # Gols sofridos
                }

        # Atualiza os gols marcados e sofridos de cada time
        stats[home]["goals_for"] += gh
        stats[home]["goals_against"] += ga
        stats[away]["goals_for"] += ga
        stats[away]["goals_against"] += gh

        # Atualiza os pontos e estatísticas com base no resultado
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

    # Se nenhum jogo válido tiver placar, mostra aviso e encerra
    if not stats:
        print("⚠️ Nenhum jogo com placar encontrado (todos podem estar agendados).")
        return

    # Converte o dicionário de estatísticas em um DataFrame
    df_stats = pd.DataFrame.from_dict(stats, orient="index").reset_index()

    # Renomeia a coluna "index" para "team"
    df_stats.rename(columns={"index": "team"}, inplace=True)

    # Calcula o saldo de gols (gols a favor - gols contra)
    df_stats["goal_difference"] = df_stats["goals_for"] - df_stats["goals_against"]

    # Calcula o número total de partidas disputadas por cada time
    df_stats["matches_played"] = df_stats["wins"] + df_stats["draws"] + df_stats["losses"]

    # Calcula a taxa de vitórias (vitórias / jogos disputados * 100)
    df_stats["win_rate_%"] = (df_stats["wins"] / df_stats["matches_played"] * 100).round(2)

    # Ordena os times como em uma classificação oficial:
    # 1º critério → pontos, 2º critério → saldo de gols
    df_stats = df_stats.sort_values(by=["points", "goal_difference"], ascending=[False, False])

    # Gera o nome do arquivo de saída com base na data de hoje
    today = datetime.today().strftime("%Y-%m-%d")
    gold_path = f"data/gold/team_performance_{competition}_{today}.csv"

    # Salva a tabela final em CSV na camada Gold
    df_stats.to_csv(gold_path, index=False, encoding="utf-8")

    # Mostra confirmação e as primeiras linhas no terminal
    print(f"✅ Métricas salvas em {gold_path}")
    print(df_stats.head())

    # Retorna o DataFrame para uso posterior (ex: dashboard)
    return df_stats

# ---------------------------------------------------------------
# Executa a função se rodar o script diretamente
# ---------------------------------------------------------------
if __name__ == "__main__":
    competition = "BSA"  # Define a competição (Brasileirão Série A)
    generate_team_metrics(competition)
