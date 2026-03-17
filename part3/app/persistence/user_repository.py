#!/usr/bin/python3
"""User-specific repository for database operations"""
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository class for User model with user-specific operations"""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Get a user by email address"""
        return self.model.query.filter_by(email=email).first()
