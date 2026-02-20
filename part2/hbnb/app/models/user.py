#!/usr/bin/python3
import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.validate()

    def validate(self):
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
