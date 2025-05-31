from models.user import User
from models.product import Product
from models.order import Order, CartItem
from models.invoice import generate_invoice
from models.shipment import Shipment

# ----------------------------
# Data loading and saving
# ----------------------------

def load_users():
    users = []
    try:
        with open('data/users.txt', 'r') as file:
            for line in file:
                users.append(User.from_line(line))
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    with open('data/users.txt', 'w') as f:
        for user in users:
            f.write(user.to_line() + '\n')

def load_products():
    products = []
    try:
        with open('data/products.txt', 'r') as file:
            for line in file:
                products.append(Product.from_line(line))
    except FileNotFoundError:
        pass
    return products

def load_orders():
    orders = []
    try:
        with open('data/orders.txt', 'r') as file:
            for line in file:
                orders.append(Order.from_line(line))
    except FileNotFoundError:
        pass
    return orders

def load_shipments():
    shipments = []
    try:
        with open('data/shipments.txt', 'r') as file:
            for line in file:
                shipments.append(Shipment.from_line(line))
    except FileNotFoundError:
        pass
    return shipments

def save_shipments(shipments):
    with open('data/shipments.txt', 'w') as f:
        for s in shipments:
            f.write(s.to_line() + '\n')

# ----------------------------
# Authentication
# ----------------------------

def register_user(users):
    username = input("Choose a username: ")
    for user in users:
        if user.username == username:
            print("Username already exists.")
            return None
    password = input("Choose a password: ")
    user = User(username, password)
    users.append(user)
    save_users(users)
    print("Registration successful.")
    return user

def login_user(users):
    username = input("Username: ")
    password = input("Password: ")
    for user in users:
        if user.username == username and user.password == password:
            print(f"Welcome back, {user.username}!")
            return user
    print("Invalid credentials.")
    return None

# ----------------------------
# Menus
# ----------------------------

def user_menu(user, products, orders, shipments):
    print(f"\nLogged in as: {user.username} ({'Admin' if user.is_admin else 'Customer'})")
    if user.is_admin:
        admin_menu(products, shipments)
    else:
        customer_menu(user, products, orders, shipments)

def admin_menu(products, shipments):
    while True:
        print("\n-- Admin Menu --")
        print("1. View Products")
        print("2. Add Product")
        print("3. View/Update Shipments")
        print("4. Logout")
        choice = input("Choose: ")

        if choice == "1":
            for p in products:
                print(f"{p.product_id} - {p.name} - ${p.price:.2f} - Stock: {p.stock} - SKU: {p.sku} - Updated: {p.last_updated}")

        elif choice == "2":
            pid = input("Product ID: ")
            name = input("Name: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))
            sku = input("SKU: ")
            products.append(Product(pid, name, price, stock, sku))

            with open('data/products.txt', 'w') as f:
                for p in products:
                    f.write(p.to_line() + '\n')

            print(f"Product '{name}' added with SKU '{sku}' at {products[-1].last_updated}.")

        elif choice == "3":
            print("\n-- Shipments --")
            if not shipments:
                print("No shipments found.")
            else:
                for idx, s in enumerate(shipments):
                    print(f"[{idx}] Order ID: {s.order_id} | User: {s.username} | Status: {s.status}")

                try:
                    index = int(input("Enter shipment index to update (or -1 to cancel): "))
                    if index == -1:
                        return
                    if 0 <= index < len(shipments):
                        new_status = input("Enter new status (Processing, Shipped, Delivered): ")
                        shipments[index].status = new_status
                        save_shipments(shipments)
                        print("✅ Shipment updated.")
                    else:
                        print("Invalid index.")
                except ValueError:
                    print("Invalid input.")

        elif choice == "4":
            break


def validate_cart(cart, products):
    for item in cart:
        matching_products = [p for p in products if p.product_id == item.product_id]
        if not matching_products:
            print(f"⚠️ Product {item.product_id} not found in stock.")
            return False
        product = matching_products[0]
        if item.quantity > product.stock:
            print(f"⚠️ Not enough stock for {product.name} (Available: {product.stock}, Requested: {item.quantity})")
            return False
    return True

def customer_menu(user, products, orders, shipments):
    cart = []
    while True:
        print("\n-- Customer Menu --")
        print("1. View All Products")
        print("2. Search Product by Name")
        print("3. Filter Products by Price Range")
        print("4. Add to Cart")
        print("5. Checkout")
        print("6. Logout")
        choice = input("Choose: ")

        if choice == "1":
            for p in products:
                print(f"{p.product_id} - {p.name} - ${p.price:.2f} - Stock: {p.stock}")

        elif choice == "2":
            keyword = input("Enter product name or keyword to search: ").lower()
            found = False
            for p in products:
                if keyword in p.name.lower():
                    print(f"{p.product_id} - {p.name} - ${p.price:.2f} - Stock: {p.stock}")
                    found = True
            if not found:
                print("No matching products found.")

        elif choice == "3":
            try:
                min_price = float(input("Minimum price: "))
                max_price = float(input("Maximum price: "))
                found = False
                for p in products:
                    if min_price <= p.price <= max_price:
                        print(f"{p.product_id} - {p.name} - ${p.price:.2f} - Stock: {p.stock}")
                        found = True
                if not found:
                    print("No products found in that price range.")
            except ValueError:
                print("Please enter valid numeric values.")

        elif choice == "4":
            pid = input("Product ID to add: ")
            quantity = int(input("Quantity: "))
            for p in products:
                if p.product_id == pid:
                    if quantity <= p.stock:
                        cart.append(CartItem(p.product_id, quantity))
                        print("Added to cart.")
                    else:
                        print("Not enough stock.")
                    break
            else:
                print("Product not found.")

        elif choice == "5":
            if not cart:
                print("Cart is empty.")
            elif not validate_cart(cart, products):
                print("❌ Order failed due to stock issues.")
            else:
                order = Order(user.username, cart)
                print("\nOrder Summary:")
                print(order.to_invoice())
                generate_invoice(order)
                orders.append(order)

                # Create and store shipment
                order_id = len(orders)  # Use index as ID
                shipment = Shipment(order_id, user.username)
                shipments.append(shipment)
                with open('data/shipments.txt', 'a') as f:
                    f.write(shipment.to_line() + '\n')

                # Update stock
                for item in cart:
                    for p in products:
                        if p.product_id == item.product_id:
                            p.stock -= item.quantity

                with open('data/products.txt', 'w') as f:
                    for p in products:
                        f.write(p.to_line() + '\n')

                with open('data/orders.txt', 'a') as f:
                    f.write(order.to_line() + '\n')

                cart.clear()
                print("✅ Order placed successfully. Shipment Status: Processing")

        elif choice == "6":
            break

# ----------------------------
# Program Entry Point
# ----------------------------

def main():
    users = load_users()
    products = load_products()
    orders = load_orders()
    shipments = load_shipments()

    print("Welcome to AWE Electronics!")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            register_user(users)
        elif choice == "2":
            user = login_user(users)
            if user:
                user_menu(user, products, orders, shipments)
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
