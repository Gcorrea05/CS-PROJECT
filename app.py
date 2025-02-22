from flask import Flask, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder='.')

def get_price_data():
    conn = sqlite3.connect('get_price.db')
    cursor = conn.cursor()
    
    # Obter a data de hoje
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Consultar o menor e o maior valor do dia de hoje
    cursor.execute('''
        SELECT MIN(lowest_price), MAX(lowest_price)
        FROM prices
        WHERE date = ?
    ''', (today,))
    
    row = cursor.fetchone()
    conn.close()
    return {"min_price": row[0], "max_price": row[1]}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prices')
def prices():
    data = get_price_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
