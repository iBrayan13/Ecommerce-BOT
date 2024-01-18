class Product:
    def __init__(self, name: str, img: str, price: float, stock: int, id= 1):
        self.id = id
        self.name = name
        self.img = img
        self.price = price
        self.stock = stock
    
class ProductOrdered(Product):
    def __init__(self, name: str, img: str, price: float, stock: int,  amount: int, id= 1):
        super().__init__(id=id, name=name, img=img, price=price, stock=stock)
        self.amount = amount