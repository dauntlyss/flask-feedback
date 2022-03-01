"""Models for Flask Feedback app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """App user model."""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed pwd & returns user."""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


