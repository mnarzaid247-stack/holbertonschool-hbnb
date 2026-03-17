#!/usr/bin/python3
"""Review-specific repository for database operations"""
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Repository class for Review model with review-specific operations"""

    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_rating(self, rating):
        """Get reviews by rating"""
        return self.model.query.filter_by(rating=rating).all()

    def get_reviews_by_rating_range(self, min_rating, max_rating):
        """Get reviews within a rating range"""
        return self.model.query.filter(
            self.model.rating >= min_rating,
            self.model.rating <= max_rating
        ).all()
