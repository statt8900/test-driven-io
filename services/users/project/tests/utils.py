# External imports

# Internal Imports
from project import db
from project.api.models import User


def add_user(username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user
