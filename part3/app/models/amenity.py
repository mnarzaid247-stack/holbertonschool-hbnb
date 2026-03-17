#!/usr/bin/python3
"""Amenity model for database persistence"""
from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model representing an amenity"""
    __tablename__ = 'amenities'

    name = db.Column(
        db.String(50),
        nullable=False
    )
    description = db.Column(
        db.Text,
        default=""
    )

    def __init__(self, name, description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.validate()

    def validate(self):
        """Validate amenity attributes"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("name cannot be empty")
        if len(self.name) > 50:
            raise ValueError("name too long")
