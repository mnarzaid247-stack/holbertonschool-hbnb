#!/usr/bin/python3
from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, user_id, place_id, rating):
        super().__init__()

        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating

        self.validate()

    def validate(self):
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("review text cannot be empty")

        if not isinstance(self.rating, int):
            raise ValueError("rating must be an integer")

        if self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")


    def update(self, data):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.validate()
        self.save()
