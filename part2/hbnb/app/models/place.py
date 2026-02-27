#!/usr/bin/python3
from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, owner_id, description="", latitude=None, longitude=None, amenity_ids=None, review_ids=None):
        super().__init__()

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        self.amenity_ids = amenity_ids or []

        self.review_ids = review_ids or []
        self.reviews = []
        self.amenities = []

        self.validate()

    def add_review(self, review):
        review_id = getattr(review, "id", review)
        if not isinstance(review_id, str) or not review_id:
            raise TypeError("review must be a Review instance or a non-empty review id string")

        if review_id in self.review_ids:
            return 

        self.review_ids.append(review_id)
        self.save()

    def add_amenity(self, amenity):
        amenity_id = getattr(amenity, "id", amenity)
        if not isinstance(amenity_id, str) or not amenity_id:
            raise TypeError("amenity must be an Amenity instance or a non-empty amenity id string")

        if amenity_id in self.amenity_ids:
            return 

        self.amenity_ids.append(amenity_id)
        self.save()

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

    def update(self, data):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.validate()
        self.save()

