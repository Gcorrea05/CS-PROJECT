import requests
import sqlite3
import time
from datetime import datetime

# Função para armazenar os dados no banco de dados
def write_to_db(conn, lowest_price, highest_price):
    cursor = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Adiciona "R$" aos valores antes de armazená-los
    lowest_price_str = f"R$ {lowest_price:.2f}".replace('.', ',')
    highest_price_str = f"R$ {highest_price:.2f}".replace('.', ',')
    
    cursor.execute('''
        INSERT INTO prices (date, time, lowest_price, highest_price)
        VALUES (?, ?, ?, ?)
    ''', (date, time_str, lowest_price_str, highest_price_str))
    
    conn.commit()

# Função para obter o preço da caixa na Steam
def get_price():
    url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=7&market_hash_name=Gallery%20Case"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # Conectar ao banco de dados uma única vez
    conn = sqlite3.connect('get_price.db')

    lowest_price_ever = float('inf')
    highest_price_ever = float('-inf')

    while True:  # Loop infinito
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                
                # Obtém o preço mais baixo e converte para float
                lowest_price = float(data.get('lowest_price', 'N/A').replace('R$', '').replace(',', '.'))

                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Preço mais baixo: R${lowest_price}")

                # Atualiza o menor e maior preço já obtido
                if lowest_price < lowest_price_ever:
                    lowest_price_ever = lowest_price
                if lowest_price > highest_price_ever:
                    highest_price_ever = lowest_price

                # Armazena no banco de dados
                write_to_db(conn, lowest_price_ever, highest_price_ever)
            else:
                print(f"Erro na requisição. Status Code: {response.status_code}")

        except Exception as e:
            print(f"Erro ao obter dados: {e}")

        # Espera 5 seg antes da próxima requisição
        time.sleep(5)

# Iniciar a coleta de preços
get_price()
