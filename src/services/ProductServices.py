from src.models.product import Product
from src.database.db_sqlite import get_connect

class ProductService:
    conexion, cursor = get_connect()

    # TODO: delete this classmethod
    @classmethod
    def set_proof_values(cls) -> bool:
        try:
            for i in range(1, 16):
                cls.cursor.execute("INSERT INTO products (name, img, price, stock) VALUES (?, ?, ?, ?)", (f"product-{i}", "https://exclusiveshopperu.com/wp-content/uploads/nike-sb-dunk-low-travis-scott-2.jpg", 6.5, 40))
            cls.conexion.commit()

            cls.cursor.execute("SELECT id FROM products LIMIT 1")
            if not cls.cursor.fetchone():
                return False
            
            return True
        
        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False

    @classmethod
    def get_all_products(cls) -> list[Product]:
        try:
            products = []

            cls.cursor.execute("SELECT id, name, img, price, stock FROM products")
            rows = cls.cursor.fetchall()
            if not rows:
                return []

            for row in rows:
                products.append(Product(
                    id= row[0],
                    name= row[1],
                    img= row[2],
                    price= row[3],
                    stock= row[4]
                ))
            
            return products
        
        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return []
        
    @classmethod
    def get_a_products(cls, id: int) -> Product:
        try:
            cls.cursor.execute("SELECT id, name, img, price, stock FROM products WHERE id = ?", (id,))
            row = cls.cursor.fetchone()
            if not row:
                return None

            return Product(
                id= row[0],
                name= row[1],
                img= row[2],
                price= row[3],
                stock= row[4]
            )
        
        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return None

    @classmethod
    def reset_products(cls) -> bool:
        try:
            cls.cursor.execute("DELETE FROM products")
            cls.conexion.commit()
            return True
        
        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False
        
    @classmethod
    def add_product(cls, product: Product) -> Product:
        try:
            sql = "INSERT INTO products (name, img, price, stock) VALUES (?, ?, ?, ?)"
            product_data = (product.name, product.img, product.price, product.stock)
            cls.cursor.execute(sql, product_data)
            if not cls.cursor.rowcount > 0:
                return None
            cls.conexion.commit()

            cls.cursor.execute(
                """SELECT id, name, img, price, stock
                FROM products
                WHERE name = ? AND img = ? AND price = ? AND stock = ?
                LIMIT 1""",
                product_data
            )
            row = cls.cursor.fetchone()
            if not row:
                return None
            
            return Product(
                id= row[0],
                name= row[1],
                img= row[2],
                price= row[3],
                stock= row[4]
            )

        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return None
        
    @classmethod
    def delete_product(cls, id: int) -> bool:
        try:
            cls.cursor.execute("DELETE FROM products WHERE id = ?", (id,))
            cls.conexion.commit()

            cls.cursor.execute("SELECT id FROM products WHERE id = ? LIMIT 1", (id,))
            if cls.cursor.fetchone():
                return False
            
            return True

        except Exception as ex:
            print(f"{type(ex)}: {ex}")
            return False