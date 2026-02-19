#!/usr/bin/python3
import uuid

class Place:
    def __init__(self, title, price, owner_id, description="", latitude=None, longitude=None, amenity_ids=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = amenity_ids or []

    def update(self, data):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
