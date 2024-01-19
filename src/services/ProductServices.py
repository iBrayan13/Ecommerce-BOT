from src.models.product import Product
import csv

class ProductService:
    csv_file = 'products.csv'

    @classmethod
    def get_all_products(cls) -> list[Product]:
        try:
            products = []

            with open(cls.csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    products.append(Product(
                        id=int(row[0]),
                        name=row[1],
                        img=row[2],
                        price=float(row[3]),
                        stock=int(row[4])
                    ))
            
            return products
        
        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return []
        
    @classmethod
    def get_a_product(cls, id: int) -> Product:
        try:
            with open(cls.csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    if int(row[0]) == id:
                        return Product(
                            id=int(row[0]),
                            name=row[1],
                            img=row[2],
                            price=float(row[3]),
                            stock=int(row[4])
                        )
            
            return None
        
        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return None

    @classmethod
    def reset_products(cls) -> bool:
        try:
            with open(cls.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'img', 'price', 'stock'])

            return True
        
        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False
        
    @classmethod
    def add_product(cls, product: Product) -> Product:
        try:
            product.name = product.name.replace("-", " ")
            product.id = len(cls.get_all_products()) + 1

            with open(cls.csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([product.id, product.name, product.img, product.price, product.stock])
            
            return product

        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return None

    @classmethod
    def change_stock(cls, id: int, new_stock: int) -> bool:
        try:
            rows = []
            with open(cls.csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                rows.append(header)

                for row in reader:
                    if int(row[0]) == id:
                        row[4] = new_stock
                    rows.append(row)

            with open(cls.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            return True

        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False
    
    @classmethod
    def change_price(cls, id: int, new_price: float) -> bool:
        try:
            rows = []
            with open(cls.csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                rows.append(header)

                for row in reader:
                    if int(row[0]) == id:
                        row[3] = new_price
                    rows.append(row)

            with open(cls.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            return True

        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False
        
    @classmethod
    def change_name(cls, id: int, new_name: str) -> bool:
        try:
            name = new_name.replace("-", " ")
            rows = []
            with open(cls.csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                rows.append(header)

                for row in reader:
                    if int(row[0]) == id:
                        row[1] = name
                    rows.append(row)

            with open(cls.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            return True

        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False
        
    @classmethod
    def delete_product(cls, id: int) -> bool:
        try:
            rows = []
            with open(cls.csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                rows.append(header)

                for row in reader:
                    if int(row[0]) != id:
                        rows.append(row)

            with open(cls.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            
            return True

        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False