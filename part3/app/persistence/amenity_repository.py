#!/usr/bin/python3
"""Amenity-specific repository for database operations"""
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Repository class for Amenity model with amenity-specific operations"""

    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Get an amenity by name"""
        return self.model.query.filter_by(name=name).first()
