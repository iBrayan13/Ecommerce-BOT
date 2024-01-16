from flask import Flask, request, render_template
from src.models.products import Product
from decouple import config
from requests import api

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
    """
    if request.method == "POST":
        url = f'https://api.telegram.org/bot{config("API_KEY")}/sendMessage'
        params = {'chat_id': request.args.get('chat_id'), 'text': request.form.get("txt")}
        api.post(url, data=params)
    """
    return render_template(
        "index.html",
        products= products_modeled,
        shopping= []
    )

if __name__ == "__main__":
    app.run(debug= True, port=5000)