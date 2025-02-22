import requests
import sqlite3
import time
from datetime import datetime

# Configurar o banco de dados
def setup_database():
    conn = sqlite3.connect('get_price.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            lowest_price TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para armazenar os dados no banco de dados
def write_to_db(conn, lowest_price):
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    cursor.execute('''
        INSERT INTO prices (date, time, lowest_price)
        VALUES (?, ?, ?)
    ''', (date, time_str, lowest_price))
    
    conn.commit()

# Função para obter o preço da caixa na Steam
def get_price():
    url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=7&market_hash_name=Gallery%20Case"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # Conectar ao banco de dados uma única vez
    conn = sqlite3.connect('get_price.db')

    while True:  # Loop infinito
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                
                # Obtém o preço mais baixo
                lowest_price = data.get('lowest_price', 'N/A')

                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Preço mais baixo: {lowest_price}")

                # Armazena no banco de dados
                write_to_db(conn, lowest_price)
            else:
                print(f"Erro na requisição. Status Code: {response.status_code}")

        except Exception as e:
            print(f"Erro ao obter dados: {e}")

        # Espera 1 minuto antes da próxima requisição
        time.sleep(5)

# Configurar o banco de dados antes de iniciar
setup_database()

# Iniciar a coleta de preços
get_price()
