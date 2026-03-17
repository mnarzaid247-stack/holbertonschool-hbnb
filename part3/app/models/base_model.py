#!/usr/bin/python3
import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """Base model for all entities with common attributes"""
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()

    def update(self, data: dict):
        """Update model attributes from a dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
