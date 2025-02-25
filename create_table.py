import sqlite3

def create_table():
    # Conectar ao banco de dados
    conn = sqlite3.connect('gallery_case.db')
    cursor = conn.cursor()

    # Criar a tabela 'prices' se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            lowest_price TEXT,
            highest_price TEXT
        )
    ''')
    conn.commit()

    # Fechar a conexão
    conn.close()
    print("Tabela 'prices' criada com sucesso!")

# Executar a função para criar a tabela
create_table()
