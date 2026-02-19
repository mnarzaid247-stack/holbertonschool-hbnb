#!/usr/bin/python3
import uuid
from datetime import datetime

class Review:
    def __init__(self, text, user_id, place_id):
        self.id = str(uuid.uuid4())
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = datetime.utcnow().isoformat()

    def update(self, data):
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
