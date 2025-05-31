from datetime import datetime

class Shipment:
    def __init__(self, order_id, username, status="Processing", created_at=None):
        self.order_id = order_id
        self.username = username
        self.status = status
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_line(self):
        return f"{self.order_id},{self.username},{self.status},{self.created_at}"

    @staticmethod
    def from_line(line):
        parts = line.strip().split(',')
        order_id, username, status = parts[0], parts[1], parts[2]
        created_at = parts[3] if len(parts) > 3 else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return Shipment(int(order_id), username, status, created_at)

    def __str__(self):
        return f"Shipment #{self.order_id} | User: {self.username} | Status: {self.status} | Created: {self.created_at}"
