class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def to_line(self):
        return f"{self.product_id},{self.name},{self.price},{self.stock}"

    @staticmethod
    def from_line(line):
        product_id, name, price, stock = line.strip().split(',')
        return Product(product_id, name, price, stock)
