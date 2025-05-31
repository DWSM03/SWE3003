from models.user import User
from models.product import Product
from models.order import Order, CartItem
from models.invoice import generate_invoice
from models.shipment import Shipment
from models.shopping_cart import ShoppingCart
from models.payment_strategy import CreditCardPayment, PayPalPayment, CashPayment


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

def generate_sales_report(orders, products):
    from collections import defaultdict

    product_sales = defaultdict(int)
    total_revenue = 0
    product_price_map = {p.product_id: p.price for p in products}

    for order in orders:
        for item in order.cart_items:
            product_sales[item.product_id] += item.quantity
            price = product_price_map.get(item.product_id, 0)
            total_revenue += price * item.quantity

    total_orders = len(orders)
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0

    print("\n📊 Sales Report")
    print("----------------------")
    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Average Order Value: ${average_order_value:.2f}")

    if product_sales:
        # Get top 3 products sorted by quantity sold
        sorted_sales = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:3]

        print("\nTop 3 Products:")
        for idx, (product_id, qty) in enumerate(sorted_sales, 1):
            product_name = next((p.name for p in products if p.product_id == product_id), "Unknown")
            print(f"{idx}. {product_name} (ID: {product_id}) - {qty} sold")
    else:
        print("No sales yet.")



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
        print("4. View Sales Report")
        print("5. Logout")
        
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
            image_url = input("Image URL (e.g., images/p001.png): ") or "no_image.png"
            category = input("Category (e.g., Laptop, Phone, Accessories): ") or "Uncategorized"

            products.append(Product(pid, name, price, stock, sku, image_url=image_url, category=category))

            with open('data/products.txt', 'w') as f:
                for p in products:
                    f.write(p.to_line() + '\n')

            print(f"✅ Product '{name}' added with image '{image_url}' at {products[-1].last_updated}.")
            print(f"✅ Product '{name}' added in category '{category}'.")



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
            generate_sales_report(load_orders(), products)
            
        elif choice == "5":
            break    

def select_payment_method():
    print("Select payment method:")
    print("1. Credit Card")
    print("2. PayPal")
    print("3. Cash")
    choice = input("Choose: ")

    if choice == "1":
        card_number = input("Card Number: ")
        card_holder = input("Card Holder Name: ")
        expiry = input("Expiry Date (MM/YY): ")
        cvv = input("CVV: ")
        return CreditCardPayment(card_number, card_holder, expiry, cvv)
    elif choice == "2":
        email = input("PayPal Email: ")
        return PayPalPayment(email)
    elif choice == "3":
        return CashPayment()
    else:
        print("Invalid payment method.")
        return None


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
    cart = ShoppingCart()
    
    def view_my_shipments(username, shipments):
        print("\n📦 Your Shipments:")
        user_shipments = [s for s in shipments if s.username == username]
        if not user_shipments:
            print("No shipments found.")
        else:
            for s in user_shipments:
                print(s)

    while True:
        print("\n-- Customer Menu --")
        print("1. View All Products")
        print("2. Search Product by Name")
        print("3. Filter Products by Price Range")
        print("4. Filter by Category")
        print("5. Add to Cart")
        print("6. Checkout")
        print("7. View My Shipments")  
        print("8. Logout")
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
            cat = input("Enter category (e.g., Laptop, Phone, etc.): ").lower()
            found = False
            for p in products:
                if p.category.lower() == cat:
                    print(f"{p.product_id} - {p.name} - ${p.price:.2f} - Stock: {p.stock} - Category: {p.category}")
                    found = True
            if not found:
                print("No products found in this category.")        

        elif choice == "5":
            pid = input("Product ID to add: ")
            quantity = int(input("Quantity: "))
            for p in products:
                if p.product_id == pid:
                    if quantity <= p.stock:
                        cart.add_item(p.product_id, quantity)

                        print("Added to cart.")
                    else:
                        print("Not enough stock.")
                    break
            else:
                print("Product not found.")

        elif choice == "6":
            if not cart:
                print("Cart is empty.")
            elif not cart.validate_cart(products):

                print("❌ Order failed due to stock issues.")
            else:
                # Calculate total price
                total_amount = sum(
                item.quantity * next((p.price for p in products if p.product_id == item.product_id), 0)
                for item in cart
                )

                print(f"\nYour total amount is: ${total_amount:.2f}")

                payment_method = select_payment_method()
                if payment_method and payment_method.pay(total_amount):
                    order = Order(user.username, cart.to_list())

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
                print(f"✅ Order placed successfully! 📦 Shipment created at {shipment.created_at}, status: {shipment.status}")

         
        elif choice == "7":
            view_my_shipments(user.username, shipments)



        elif choice == "8":
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
