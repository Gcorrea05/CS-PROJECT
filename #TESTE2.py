import requests
import time
import csv
from datetime import datetime

def write_to_csv(lowest_price, volume, median_price):
    with open('gallery_case_prices.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([lowest_price, volume, median_price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def get_gallery_case_price():
    url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=7&market_hash_name=Gallery%20Case"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    params = {
        'appid': 730,  # App ID para CS:GO/CS2
        'currency': 7,  # Moeda: 7 é BRL
    }

    # Adicionar cabeçalhos (se necessário)
    with open('gallery_case_prices.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Preço mais baixo", "Volume", "Preço mediano", "Timestamp"])

    for _ in range(10):
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            try:
                # Acessando os valores desejados
                lowest_price = data.get('lowest_price', 'N/A')
                volume = data.get('volume', 'N/A')
                median_price = data.get('median_price', 'N/A')
                print(f"Preço mais baixo: {lowest_price}")
                print(f"Volume: {volume}")
                print(f"Preço mediano: {median_price}")
                
                # Armazenando os dados no arquivo CSV
                write_to_csv(lowest_price, volume, median_price)
            except KeyError:
                print("Erro: Não foi possível encontrar as informações solicitadas.")
        else:
            print("Erro ao fazer a requisição. Status Code:", response.status_code)
        
        # Esperar 5 segundos antes de fazer a próxima requisição
        time.sleep(5)

# Chame a função
get_gallery_case_price()

''' 
colocar a parte da analise e automatizar tudo, 
FLASK API
STEAM WEB API
PYTHON 
PANDAS
PY.PLOT
CALCULO
API REQUEST NO PYTHON

*NAO USAR WEBSCRAPING
'''
