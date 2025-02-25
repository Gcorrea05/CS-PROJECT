import requests
import sqlite3
import time
from datetime import datetime

# Função para armazenar os dados no banco de dados
def write_to_db(conn, date, time_str, lowest_price, highest_price):
    cursor = conn.cursor()

    # Adiciona "R$" aos valores antes de armazená-los
    lowest_price_str = f"{lowest_price:.2f}".replace('.', ',')
    highest_price_str = f"{highest_price:.2f}".replace('.', ',')

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
    conn = sqlite3.connect('gallery_case.db')

    # Verificar a data atual no início
    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor = conn.cursor()
    cursor.execute('SELECT MIN(lowest_price), MAX(lowest_price) FROM prices WHERE date = ?', (current_date,))
    row = cursor.fetchone()
    lowest_price_today = float('inf')
    highest_price_today = float('-inf')
    
    if row[0] is not None and row[1] is not None:
        lowest_price_today = float(row[0].replace(',', '.'))
        highest_price_today = float(row[1].replace(',', '.'))

    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 429:
                print("Muitas requisições! Aguardando 10 minutos antes de tentar novamente...")
                time.sleep(300)  # Espera 5 minutos antes de tentar novamente
                continue
            
            if response.status_code == 200:
                data = response.json()
                
                # Obtém o preço mais baixo e converte para float
                lowest_price = float(data.get('lowest_price', 'N/A').replace('R$', '').replace(',', '.'))

                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Preço mais baixo: R${lowest_price}")

                # Verifica se o dia mudou
                now = datetime.now()
                new_date = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")
                
                if new_date != current_date:
                    current_date = new_date
                    lowest_price_today = lowest_price
                    highest_price_today = lowest_price
                else:
                    if lowest_price < lowest_price_today:
                        lowest_price_today = lowest_price
                    if lowest_price > highest_price_today:
                        highest_price_today = lowest_price
                
                # Armazena no banco de dados
                write_to_db(conn, current_date, time_str, lowest_price_today, highest_price_today)
            else:
                print(f"Erro na requisição. Status Code: {response.status_code}")

        except Exception as e:
            print(f"Erro ao obter dados: {e}")

        # Espera 60 segundos antes da próxima requisição
        time.sleep(60)

# Iniciar a coleta de preços
get_price()
