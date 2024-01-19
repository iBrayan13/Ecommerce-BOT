from src.models.product import ProductOrdered
from datetime import datetime

class Order:
    def __init__(self, username: str, products: list[ProductOrdered]):
        self.username = username
        self.products = products
        self.canceled = False
        
        datenow = datetime.utcnow()
        self.date = datetime(datenow.year, datenow.month, datenow.day, datenow.hour, datenow.minute)
        