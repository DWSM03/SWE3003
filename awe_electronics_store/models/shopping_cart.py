from models.order import CartItem

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product_id, quantity):
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                return
        self.items.append(CartItem(product_id, quantity))

    def clear(self):
        self.items = []

    def validate_cart(self, products):
        for item in self.items:
            matching = [p for p in products if p.product_id == item.product_id]
            if not matching:
                print(f"⚠️ Product {item.product_id} not found.")
                return False
            product = matching[0]
            if item.quantity > product.stock:
                print(f"⚠️ Not enough stock for {product.name} (Available: {product.stock}, Requested: {item.quantity})")
                return False
        return True

    def to_list(self):
        return self.items

    def __iter__(self):
        return iter(self.items)  # ✅ This fixes the for-loop error!
