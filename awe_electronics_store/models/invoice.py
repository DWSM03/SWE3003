def generate_invoice(order):
    print("\n--- Invoice ---")
    print(order.to_invoice())
    print("Payment Status: ✅ Payment processed successfully ")
    print("---------------\n")
