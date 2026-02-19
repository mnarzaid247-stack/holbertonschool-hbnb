#!/usr/bin/python3
from app.models.place import Place
from app.models.review import Review

def _validate_price(price):
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError("price must be a number")
    if p <= 0:
        raise ValueError("price must be > 0")
    return p

def _validate_lat_lon(lat, lon):
    if lat is not None:
        lat = float(lat)
        if lat < -90 or lat > 90:
            raise ValueError("latitude must be between -90 and 90")
    if lon is not None:
        lon = float(lon)
        if lon < -180 or lon > 180:
            raise ValueError("longitude must be between -180 and 180")

class HBnBFacade:
    def __init__(self, user_repo, amenity_repo, place_repo, review_repo):
        self.users = user_repo
        self.amenities = amenity_repo
        self.places = place_repo
        self.reviews = review_repo

    # ---------- USERS / AMENITIES (already used by your APIs) ----------
    def get_all_users(self):
        return self.users.get_all()

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_user_by_email(self, email):
        return self.users.get_by_attribute("email", email)

    def create_user(self, data):
        # your existing logic likely lives elsewhere; keep as-is
        return self.users.add(data)

    def update_user(self, user_id, data):
        return self.users.update(user_id, data)

    def get_all_amenities(self):
        return self.amenities.get_all()

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def create_amenity(self, data):
        return self.amenities.add(data)

    def update_amenity(self, amenity_id, data):
        return self.amenities.update(amenity_id, data)

    # ---------- PLACES ----------
    def create_place(self, data):
        for k in ("title", "price", "owner_id"):
            if k not in data or data[k] in (None, ""):
                raise ValueError(f"Missing required field: {k}")

        owner = self.users.get(data["owner_id"])
        if not owner:
            raise LookupError("Owner not found")

        price = _validate_price(data["price"])
        _validate_lat_lon(data.get("latitude"), data.get("longitude"))

        amenity_ids = data.get("amenity_ids", [])
        for aid in amenity_ids:
            if not self.amenities.get(aid):
                raise LookupError(f"Amenity not found: {aid}")

        place = Place(
            title=data["title"],
            description=data.get("description", ""),
            price=price,
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=data["owner_id"],
            amenity_ids=amenity_ids,
        )
        self.places.add(place)
        return place

    def get_place(self, place_id):
        return self.places.get(place_id)

    def get_all_places(self):
        return self.places.get_all()

    def update_place(self, place_id, data):
        place = self.places.get(place_id)
        if not place:
            return None

        if "owner_id" in data:
            raise ValueError("owner_id cannot be updated")

        if "price" in data:
            data["price"] = _validate_price(data["price"])

        if "latitude" in data or "longitude" in data:
            _validate_lat_lon(
                data.get("latitude", place.latitude),
                data.get("longitude", place.longitude)
            )

        if "amenity_ids" in data:
            amenity_ids = data["amenity_ids"] or []
            for aid in amenity_ids:
                if not self.amenities.get(aid):
                    raise LookupError(f"Amenity not found: {aid}")
            data["amenity_ids"] = amenity_ids

        return self.places.update(place_id, data)

    # ---------- REVIEWS ----------
    def create_review(self, data):
        for k in ("text", "user_id", "place_id"):
            if k not in data or data[k] in (None, ""):
                raise ValueError(f"Missing required field: {k}")

        text = data["text"].strip()
        if not text:
            raise ValueError("text cannot be empty")

        if not self.users.get(data["user_id"]):
            raise LookupError("User not found")

        if not self.places.get(data["place_id"]):
            raise LookupError("Place not found")

        review = Review(text=text, user_id=data["user_id"], place_id=data["place_id"])
        self.reviews.add(review)
        return review

    def get_review(self, review_id):
        return self.reviews.get(review_id)

    def get_all_reviews(self):
        return self.reviews.get_all()

    def update_review(self, review_id, data):
        review = self.reviews.get(review_id)
        if not review:
            return None

        if "user_id" in data or "place_id" in data:
            raise ValueError("user_id/place_id cannot be updated")

        if "text" in data:
            text = (data["text"] or "").strip()
            if not text:
                raise ValueError("text cannot be empty")
            data["text"] = text

        return self.reviews.update(review_id, data)

    def delete_review(self, review_id):
        return self.reviews.delete(review_id)

    def get_reviews_by_place(self, place_id):
        # simple in-memory filter
        return [r for r in self.reviews.get_all() if r.place_id == place_id]

    # ---------- SERIALIZATION HELPERS ----------
    def serialize_place(self, place):
        owner = self.users.get(place.owner_id)
        owner_dict = None
        if owner:
            owner_dict = {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            }

        amenities = []
        for aid in place.amenity_ids:
            a = self.amenities.get(aid)
            if a:
                amenities.append({"id": a.id, "name": a.name})

        reviews = [
            {"id": r.id, "text": r.text, "user_id": r.user_id, "place_id": r.place_id, "created_at": r.created_at}
            for r in self.get_reviews_by_place(place.id)
        ]

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_dict,
            "amenities": amenities,
            "reviews": reviews,
        }

    def serialize_review(self, review):
        return {
            "id": review.id,
            "text": review.text,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "created_at": review.created_at,
        }
#we NEED to talk about this later!!
