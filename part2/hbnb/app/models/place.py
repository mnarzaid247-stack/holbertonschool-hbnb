#!/usr/bin/python3
from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, price, owner_id, description="", latitude=None, longitude=None, amenity_ids=None):
        super().__init__()

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = amenity_ids or []

        self.validate()

    def validate(self):
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

