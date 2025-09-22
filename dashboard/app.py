import os
import pandas as pd
import streamlit as st
from datetime import datetime

# Função para carregar o arquivo mais recente da camada Gold (apenas BSA)
def load_latest_gold():
    gold_path = "data/gold"
    files = [f for f in os.listdir(gold_path) if f.startswith("team_performance_BSA")]
    
    if not files:
        st.error(f"Nenhum arquivo encontrado em {gold_path} para o Brasileirão (BSA)")
        return None
    
    latest_file = sorted(files)[-1]  # Pega o arquivo mais recente
    file_path = os.path.join(gold_path, latest_file)
    
    return pd.read_csv(file_path)

# ---------------------- STREAMLIT APP ----------------------

st.set_page_config(page_title="Football Analytics - Brasileirão", layout="wide")

st.title("🇧🇷 Brasileirão Série A - Dashboard")
st.markdown("### Monitoramento de desempenho dos times (Camada Gold)")

# Carregar dados do Gold
df = load_latest_gold()

if df is not None:
    # Exibir tabela completa
    st.subheader("📊 Classificação dos Times")
    st.dataframe(df)

    # Gráfico de pontos
    st.subheader("🏆 Pontos por Time")
    st.bar_chart(df.set_index("team")["points"])

    # Gráfico de gols
    st.subheader("⚡ Saldo de Gols")
    st.bar_chart(df.set_index("team")["goal_difference"])

    # Taxa de vitórias
    st.subheader("✅ Taxa de Vitórias (%)")
    st.bar_chart(df.set_index("team")["win_rate_%"])
