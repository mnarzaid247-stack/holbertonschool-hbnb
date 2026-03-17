#!/usr/bin/python3
import re
from app import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    """User model representing a user in the system"""
    __tablename__ = 'users'

    first_name = db.Column(
        db.String(50),
        nullable=False
    )
    last_name = db.Column(
        db.String(50),
        nullable=False
    )
    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(128),
        nullable=False
    )
    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_admin=False
    ):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None
        if password:
            self.hash_password(password)
        self.validate()

    def hash_password(self, password):
        """Hash the password before storing it"""
        self.password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

    def verify_password(self, password):
        """Verify if the provided password matches the hashed password"""
        return bcrypt.check_password_hash(self.password, password)

    def validate(self):
        """Validate user attributes"""
        if not self.first_name or len(self.first_name.strip()) == 0:
            raise ValueError("first_name cannot be empty")

        if not self.last_name or len(self.last_name.strip()) == 0:
            raise ValueError("last_name cannot be empty")

        if not self.email or len(self.email.strip()) == 0:
            raise ValueError("email cannot be empty")

        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_regex, self.email):
            raise ValueError("invalid email format")

        if len(self.first_name) > 50:
            raise ValueError("first_name too long")

        if len(self.last_name) > 50:
            raise ValueError("last_name too long")
