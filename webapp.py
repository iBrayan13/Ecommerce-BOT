from flask import Flask, render_template
from src.services.ProductServices import ProductService

app = Flask(__name__)
service_product = ProductService()

@app.route("/shop", methods=["GET", "POST"])
def shop():

    return render_template(
        "index.html",
        products= service_product.get_all_products()
    )

if __name__ == "__main__":
    app.run(debug= True, port=5000)