from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number, card_holder, expiry, cvv):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiry = expiry
        self.cvv = cvv
    
    def pay(self, amount):
        print(f"Paid ${amount:.2f} using Credit Card ending with {self.card_number[-4:]}")
        return True

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        print(f"Paid ${amount:.2f} using PayPal account {self.email}")
        return True

class CashPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ${amount:.2f} in cash")
        return True
