from datetime import datetime

class Product:
    def __init__(self, product_id, name, price, stock, sku, last_updated=None):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.sku = sku
        self.last_updated = last_updated or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_line(self):
        return f"{self.product_id},{self.name},{self.price},{self.stock},{self.sku},{self.last_updated}"

    @staticmethod
    def from_line(line):
        parts = line.strip().split(',')
        if len(parts) == 6:
            product_id, name, price, stock, sku, last_updated = parts
        elif len(parts) == 4:
            # Backward compatibility: older format with no SKU or timestamp
            product_id, name, price, stock = parts
            sku = "UNKNOWN"
            last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError(f"Invalid product line: {line.strip()}")
        
        return Product(product_id, name, price, stock, sku, last_updated)
