from datetime import datetime

class Product:
    def __init__(self, product_id, name, price, stock, sku="UNKNOWN", last_updated=None, image_url="no_image.png", category="Uncategorized"):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.sku = sku
        self.last_updated = last_updated or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.image_url = image_url
        self.category = category

    def to_line(self):
        return f"{self.product_id},{self.name},{self.price},{self.stock},{self.sku},{self.last_updated},{self.image_url},{self.category}"

    @staticmethod
    def from_line(line):
        parts = line.strip().split(',')
        if len(parts) == 8:
            product_id, name, price, stock, sku, last_updated, image_url, category = parts
        elif len(parts) == 7:
            product_id, name, price, stock, sku, last_updated, image_url = parts
            category = "Uncategorized"
        elif len(parts) == 6:
            product_id, name, price, stock, sku, last_updated = parts
            image_url = "no_image.png"
            category = "Uncategorized"
        elif len(parts) == 4:
            product_id, name, price, stock = parts
            sku = "UNKNOWN"
            last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            image_url = "no_image.png"
            category = "Uncategorized"
        else:
            raise ValueError(f"Invalid product line: {line.strip()}")

        return Product(product_id, name, price, stock, sku, last_updated, image_url, category)
