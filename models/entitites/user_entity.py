from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password, confirmed, token) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.confirmed = confirmed
        self.token = token
