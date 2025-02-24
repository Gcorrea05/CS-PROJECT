import sqlite3

def clear_database():
    # Conectar ao banco de dados
    conn = sqlite3.connect('get_price.db')
    cursor = conn.cursor()
    
    # Excluir todos os registros da tabela 'prices'
    cursor.execute('DELETE FROM prices')
    conn.commit()
    
    # Fechar a conexão
    conn.close()
    print("Banco de dados limpo com sucesso!")

# Executar a função para limpar o banco de dados
clear_database()
