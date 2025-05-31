from models.user import User
from models.product import Product
from models.order import Order, CartItem
from models.invoice import generate_invoice

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
        pass  # File may not exist yet
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

def user_menu(user, products, orders):
    print(f"\nLogged in as: {user.username} ({'Admin' if user.is_admin else 'Customer'})")
    if user.is_admin:
        admin_menu(products)
    else:
        customer_menu(user, products, orders)

def admin_menu(products):
    while True:
        print("\n-- Admin Menu --")
        print("1. View Products")
        print("2. Add Product")
        print("3. Logout")
        choice = input("Choose: ")
        if choice == "1":
            for p in products:
                print(f"{p.product_id} - {p.name} - ${p.price} - Stock: {p.stock}")
        elif choice == "2":
            pid = input("Product ID: ")
            name = input("Name: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))
            products.append(Product(pid, name, price, stock))
            with open('data/products.txt', 'w') as f:
                for p in products:
                    f.write(p.to_line() + '\n')
            print("Product added.")
        elif choice == "3":
            break

def customer_menu(user, products, orders):
    cart = []
    while True:
        print("\n-- Customer Menu --")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. Checkout")
        print("4. Logout")
        choice = input("Choose: ")
        if choice == "1":
            for p in products:
                print(f"{p.product_id} - {p.name} - ${p.price} - Stock: {p.stock}")
        elif choice == "2":
            pid = input("Product ID to add: ")
            quantity = int(input("Quantity: "))
            for p in products:
                if p.product_id == pid:
                    if quantity <= p.stock:
                        cart.append(CartItem(p.product_id, quantity))
                        print("Added to cart.")
                    else:
                        print("Not enough stock.")
        elif choice == "3":
            if not cart:
                print("Cart is empty.")
            else:
                order = Order(user.username, cart)
                print("\nOrder Summary:")
                print(order.to_invoice())
                generate_invoice(order)
                orders.append(order)
                with open('data/orders.txt', 'a') as f:
                    f.write(order.to_line() + '\n')
                cart.clear()
        elif choice == "4":
            break

# ----------------------------
# Program Entry Point
# ----------------------------

def main():
    users = load_users()
    products = load_products()
    orders = load_orders()

    print("Welcome to AWE Electronics!")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            register_user(users)
        elif choice == "2":
            user = login_user(users)
            if user:
                user_menu(user, products, orders)
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
