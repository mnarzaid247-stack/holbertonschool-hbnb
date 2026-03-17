#!/usr/bin/python3
"""Place model for database persistence"""
from app import db
from app.models.base_model import BaseModel


class Place(BaseModel):
    """Place model representing a rental property"""
    __tablename__ = 'places'

    title = db.Column(
        db.String(100),
        nullable=False
    )
    description = db.Column(
        db.Text,
        default=""
    )
    price = db.Column(
        db.Float,
        nullable=False
    )
    latitude = db.Column(
        db.Float
    )
    longitude = db.Column(
        db.Float
    )
    owner_id = db.Column(
        db.String(36),
        nullable=False
    )
    is_available = db.Column(
        db.Boolean,
        default=True
    )

    def __init__(
        self,
        title,
        price,
        owner_id,
        description="",
        latitude=None,
        longitude=None,
        is_available=True
    ):
        super().__init__()
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.is_available = is_available
        self.validate()

    def validate(self):
        """Validate place attributes"""
        if not self.owner_id or len(self.owner_id.strip()) == 0:
            raise ValueError("owner_id cannot be empty")

        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("title cannot be empty")

        if len(self.title) > 100:
            raise ValueError("title too long")

        if self.price <= 0:
            raise ValueError("price must be positive")

        if self.latitude is not None:
            if self.latitude < -90 or self.latitude > 90:
                raise ValueError("invalid latitude")

        if self.longitude is not None:
            if self.longitude < -180 or self.longitude > 180:
                raise ValueError("invalid longitude")
