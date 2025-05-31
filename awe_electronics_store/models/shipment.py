class Shipment:
    def __init__(self, order_id, username, status="Processing"):
        self.order_id = order_id
        self.username = username
        self.status = status

    def to_line(self):
        return f"{self.order_id},{self.username},{self.status}"

    @staticmethod
    def from_line(line):
        order_id, username, status = line.strip().split(',')
        return Shipment(int(order_id), username, status)
