class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def to_line(self):
        return f"{self.username},{self.password},{self.is_admin}"

    @staticmethod
    def from_line(line):
        username, password, is_admin = line.strip().split(',')
        return User(username, password, is_admin == 'True')
