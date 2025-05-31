class CartItem:
    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = int(quantity)

class Order:
    def __init__(self, username, cart_items):
        self.username = username
        self.cart_items = cart_items

    def to_line(self):
        items = ','.join(f"{item.product_id}:{item.quantity}" for item in self.cart_items)
        return f"{self.username}|{items}"

    @staticmethod
    def from_line(line):
        username, item_data = line.strip().split('|')
        items = [CartItem(pid_qty.split(':')[0], int(pid_qty.split(':')[1])) for pid_qty in item_data.split(',')]
        return Order(username, items)

    def to_invoice(self):
        return "\n".join([f"{item.product_id} x{item.quantity}" for item in self.cart_items])
