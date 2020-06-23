from flask_login import UserMixin

# users = {'foo@bar.tld': {'password': 'secret', 'category': 'admin'}}
users = {'foo@bar.tld': {'password': 'secret', 'category': 'user'}}


class User(UserMixin):
    pass
