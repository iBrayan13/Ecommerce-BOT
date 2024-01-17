from flask import Flask, render_template
from src.models.product import Product
import sqlite3

app = Flask(__name__)
conexion = sqlite3.connect('bot_ecommerce.db')
cursor = conexion.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    img TEXT,
    price FLOAT,
    stock INTEGER
)''')

cursor.execute("SELECT id, name, img, price, stock FROM products")
rows = cursor.fetchall()
if not rows:
    for i in range(1, 16):
        cursor.execute("INSERT INTO products (name, img, price, stock) VALUES (?, ?, ?, ?)", (f"product-{i}", "https://exclusiveshopperu.com/wp-content/uploads/nike-sb-dunk-low-travis-scott-2.jpg", 6.5, 40))
    conexion.commit()

    cursor.execute("SELECT id, name, img, price, stock FROM products")
    rows = cursor.fetchall()

@app.route("/shop", methods=["GET", "POST"])
def shop():
    products_modeled = []
    for row in rows:
        products_modeled.append(Product(
            id= row[0],
            name= f"{row[1]}",
            img= f"{row[2]}",
            price= row[3],
            stock= row[4]
        ))

    return render_template(
        "index.html",
        products= products_modeled,
        shopping= []
    )

if __name__ == "__main__":
    app.run(debug= True, port=5000)