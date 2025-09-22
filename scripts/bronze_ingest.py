import requests #Biblioteca para fazer chamadas HTTP (buscar dados da API)
import pandas as pd #Transformar dados em tabelas
import os # Criar diretórios e manipuar caminhos de arquivos
from datetime import datetime #Para gerar datas

import sys, os

# Adiciona a raiz do projeto ao sys.path (um nível acima da pasta scripts)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import API_KEY, BASE_URL #Importa as configs da API

# Função que vai buscar os dados da API

def get_matches( competition='BSA', season=2025):

# Busca partidas do Brasileirão

    #Monta a URL da API
    url = f"{BASE_URL}/competitions/{competition}/matches?season={season}"

    #Cabeçalho com a chave da API
    headers = {"X-Auth-Token": API_KEY}

    print(f"🔗 Requisitando URL: {url}")   # Debug
    #Faz a requisição para a API
    response = requests.get(url, headers=headers)

    print(f"📡 Status da resposta: {response.status_code}")  # Debug

    print("❌ Erro na API:", response.text)  # Debug
    #Se der erro (código diferente de 200), lança uma excessão com detalhes
    if response.status_code !=200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")

    #Retorna os dados no formato JSON
    return response.json()


#Função para salvar os dados crus na camada Bronze
def save_bronze(data, competition="BSA"):

    #Garante que a pasta 'data/bronze' exista (se não, vai criar)
    os.makedirs("data/bronze", exist_ok=True)

    #Cria uma string com a data de hoje
    today = datetime.today().strftime("%Y-%m-%d")

    #Define o caminho onde os dados serão salvos
    file_patch = f"data/bronze/matches_{competition}_{today}.json"

    #Abre o arquivo em modo esceita e salva os dados em JSON
    with open(file_patch, "w", encoding="utf-8") as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=4)


    print(f"Dados salvos em {file_patch}")

#Só roda se o script for executado diretamente
if __name__ == "__main__":
    #Pegando as partidas de 2025
    competition = "BSA"
    season = 2025

    print("🚀 Iniciando coleta de dados...")  # Debug
    #Busca os dados de partidas na API
    matches = get_matches(competition, season)

    print("💾 Salvando dados no Bronze...")   # Debug
    #Salva esses dados crus na camada Bronze
    save_bronze(matches, competition)