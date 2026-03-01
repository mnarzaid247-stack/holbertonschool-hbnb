#!/usr/bin/python3
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ---------- Users ----------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "password" in user_data:
            user.hash_password(user_data["password"])
            user_data = {k: v for k, v in user_data.items() if k != "password"}
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    # ---------- Amenities ----------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # ---------- Places ----------
    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        if not owner_id or not self.get_user(owner_id):
            raise ValueError("owner_id does not reference an existing user")

        amenity_ids = place_data.get("amenity_ids") or []
        for aid in amenity_ids:
            if not self.get_amenity(aid):
                raise ValueError(f"amenity_id does not reference an existing amenity: {aid}")

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description", ""),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner_id=owner_id,
            amenity_ids=amenity_ids,
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "owner_id" in place_data:
            if not self.get_user(place_data["owner_id"]):
                raise ValueError("owner_id does not reference an existing user")

        if "amenity_ids" in place_data:
            for aid in (place_data.get("amenity_ids") or []):
                if not self.get_amenity(aid):
                    raise ValueError(f"amenity_id does not reference an existing amenity: {aid}")

        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    # ---------- Reviews ----------
    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if not user_id or not self.get_user(user_id):
            raise ValueError("user_id does not reference an existing user")

        if not place_id or not self.get_place(place_id):
            raise ValueError("place_id does not reference an existing place")

        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            user_id=user_id,
            place_id=place_id,
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # do NOT allow changing relationships in update (keeps it simple + safe)
        if "user_id" in review_data or "place_id" in review_data:
            raise ValueError("Cannot update user_id or place_id")

        # validate rating/text using Review.validate() by setting then validating
        if "text" in review_data:
            review.text = review_data["text"]
        if "rating" in review_data:
            review.rating = review_data["rating"]

        review.validate()
        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
