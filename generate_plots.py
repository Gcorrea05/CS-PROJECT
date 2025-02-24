import sqlite3
import plotly.graph_objects as go
from datetime import datetime

# Função para obter os preços por hora
def get_prices_per_hour():
    conn = sqlite3.connect('gallery_case.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%H', time) AS hour, MAX(highest_price), MIN(lowest_price)
        FROM prices
        GROUP BY hour
        ORDER BY hour
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

# Função para gerar gráficos interativos
def plot_prices():
    data = get_prices_per_hour()
    
    # Extrair as horas, preços máximos e mínimos
    hours = [row[0] for row in data]
    max_prices = [float(row[1].replace(',', '.')) for row in data]
    min_prices = [float(row[2].replace(',', '.')) for row in data]

    # Gráfico de Preços Máximos por Hora
    fig_max = go.Figure()
    fig_max.add_trace(go.Scatter(x=hours, y=max_prices, mode='lines+markers', name='Preço Máximo',
                                 marker=dict(color='red'), line=dict(color='red')))
    fig_max.update_layout(title='Preços Máximos por Hora', xaxis_title='Hora', yaxis_title='Preço (R$)',
                          template='plotly_dark')
    fig_max.update_traces(text=[f'{p:.2f}' for p in max_prices], hoverinfo='text')
    fig_max.write_html('precos_maximos_por_hora.html')

    # Gráfico de Preços Mínimos por Hora
    fig_min = go.Figure()
    fig_min.add_trace(go.Scatter(x=hours, y=min_prices, mode='lines+markers', name='Preço Mínimo',
                                 marker=dict(color='blue'), line=dict(color='blue')))
    fig_min.update_layout(title='Preços Mínimos por Hora', xaxis_title='Hora', yaxis_title='Preço (R$)',
                          template='plotly_dark')
    fig_min.update_traces(text=[f'{p:.2f}' for p in min_prices], hoverinfo='text')
    fig_min.write_html('precos_minimos_por_hora.html')

# Chamar a função para gerar os gráficos
plot_prices()
