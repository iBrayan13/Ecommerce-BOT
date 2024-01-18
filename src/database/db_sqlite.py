import sqlite3

def get_connect():
    conexion = sqlite3.connect('./bot_ecommerce.db')
    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        img TEXT,
        price FLOAT,
        stock INTEGER
    )''')

    return conexion, cursor