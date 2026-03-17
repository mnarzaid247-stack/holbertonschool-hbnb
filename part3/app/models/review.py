#!/usr/bin/python3
"""Review model for database persistence"""
from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review model representing a user review"""
    __tablename__ = 'reviews'

    text = db.Column(
        db.Text,
        nullable=False
    )
    rating = db.Column(
        db.Integer,
        nullable=False
    )
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
    )
    place_id = db.Column(
        db.String(36),
        db.ForeignKey('places.id'),
        nullable=False
    )

    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        self.validate()

    def validate(self):
        """Validate review attributes"""
        if not self.user_id or len(self.user_id.strip()) == 0:
            raise ValueError("user_id cannot be empty")

        if not self.place_id or len(self.place_id.strip()) == 0:
            raise ValueError("place_id cannot be empty")

        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("review text cannot be empty")

        if not isinstance(self.rating, int):
            raise ValueError("rating must be an integer")

        if self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")
