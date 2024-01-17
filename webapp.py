from flask import Flask, render_template
from src.models.product import Product

app = Flask(__name__)

@app.route("/shop", methods=["GET", "POST"])
def shop():
    products_modeled = []
    for i in range(1, 21):
        products_modeled.append(Product(
            id= i,
            name= f"product-{i}",
            img= "https://exclusiveshopperu.com/wp-content/uploads/nike-sb-dunk-low-travis-scott-2.jpg",
            price= 7.5,
            stock= 35
        ))

    return render_template(
        "index.html",
        products= products_modeled,
        shopping= []
    )

if __name__ == "__main__":
    app.run(debug= True, port=5000)