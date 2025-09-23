import os
import pandas as pd
import streamlit as st

# ---------------------- Funções utilitárias ----------------------

# Carregar o arquivo mais recente de classificação (Gold - Times)
def load_latest_team_performance():
    gold_path = "data/gold"
    files = [f for f in os.listdir(gold_path) if f.startswith("team_performance_BSA")]
    if not files:
        return None
    latest_file = sorted(files)[-1]
    return pd.read_csv(os.path.join(gold_path, latest_file))

# Carregar o arquivo mais recente de artilheiros (Gold - Jogadores)
def load_latest_scorers():
    gold_path = "data/gold"
    files = [f for f in os.listdir(gold_path) if f.startswith("scorers_BSA")]
    if not files:
        return None
    latest_file = sorted(files)[-1]
    return pd.read_csv(os.path.join(gold_path, latest_file))

# ---------------------- STREAMLIT APP ----------------------

st.set_page_config(page_title="Football Analytics - Brasileirão", layout="wide")

st.title("🇧🇷 Brasileirão Série A - Dashboard")
st.markdown("### Monitoramento do Campeonato (Camada Gold)")

# Criar abas
tab1, tab2 = st.tabs(["📊 Classificação dos Times", "🥇 Artilheiros e Assistências"])

# ---------------------- Aba 1: Classificação ----------------------
with tab1:
    df = load_latest_team_performance()
    if df is None:
        st.error("Nenhum arquivo de classificação encontrado em data/gold")
    else:
        st.subheader("📊 Classificação dos Times")
        st.dataframe(df)

        # Gráfico de pontos
        st.subheader("🏆 Pontos por Time")
        st.bar_chart(df.set_index("team")["points"])

        # Gráfico de saldo de gols
        st.subheader("⚡ Saldo de Gols")
        st.bar_chart(df.set_index("team")["goal_difference"])

        # Gráfico de taxa de vitórias
        st.subheader("✅ Taxa de Vitórias (%)")
        st.bar_chart(df.set_index("team")["win_rate_%"])

# ---------------------- Aba 2: Artilheiros ----------------------
with tab2:
    scorers = load_latest_scorers()
    if scorers is None:
        st.error("Nenhum arquivo de artilheiros encontrado em data/gold")
    else:
        st.subheader("🏆 Ranking de Artilheiros")
        st.dataframe(scorers)

        # Gráfico de gols por jogador
        st.subheader("⚽ Gols por Jogador")
        st.bar_chart(scorers.set_index("player")["goals"])

        # Se houver assistências, mostrar gráfico
        if "assists" in scorers.columns and scorers["assists"].notna().any():
            st.subheader("🎯 Assistências por Jogador")
            st.bar_chart(scorers.set_index("player")["assists"])
