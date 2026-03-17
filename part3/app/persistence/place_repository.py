#!/usr/bin/python3
"""Place-specific repository for database operations"""
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Repository class for Place model with place-specific operations"""

    def __init__(self):
        super().__init__(Place)

    def get_places_by_title(self, title):
        """Get places by title (partial match)"""
        return self.model.query.filter(
            self.model.title.contains(title)
        ).all()

    def get_places_by_price_range(self, min_price, max_price):
        """Get places within a price range"""
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()
