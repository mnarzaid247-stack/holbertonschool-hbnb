#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace("places", description="Place operations")

# related models (for swagger)
amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
    },
)

review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(description="Review ID"),
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating of the place (1-5)"),
        "user_id": fields.String(description="ID of the user"),
        "place_id": fields.String(description="ID of the place"),
    },
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(
            required=True,
            description="Title of the place"
        ),
        "description": fields.String(
            description="Description of the place"
        ),
        "price": fields.Float(
            required=True,
            description="Price per night"
        ),
        "latitude": fields.Float(
            description="Latitude of the place"
        ),
        "longitude": fields.Float(
            description="Longitude of the place"
        ),
        "owner_id": fields.String(
            required=True,
            description="ID of the owner (User)"
        ),
        "is_available": fields.Boolean(
            description="Availability status of the place"
        ),
    },
)


def place_to_dict(place):
    owner = facade.get_user(place.owner_id) if getattr(place, "owner_id", None) else None

    amenities = []
    for aid in getattr(place, "amenity_ids", []) or []:
        a = facade.get_amenity(aid)
        if a:
            amenities.append({"id": a.id, "name": a.name})

    reviews = []
    try:
        place_reviews = facade.get_reviews_by_place(place.id)
        for review in place_reviews:
            user = facade.get_user(review.user_id) if getattr(review, "user_id", None) else None
            reviews.append({
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id,
                "user_name": (
                    f"{user.first_name} {user.last_name}".strip()
                    if user else "Anonymous"
                )
            })
    except Exception:
        reviews = []

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": (
            {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            }
            if owner
            else None
        ),
        "amenities": amenities,
        "reviews": reviews,
        "is_available": getattr(place, "is_available", True),
    }


@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner not found")
    def post(self):
        """Register a new place"""
        place_data = api.payload

        # Validate owner exists
        owner = facade.get_user(place_data["owner_id"])
        if not owner:
            return {"error": "Owner not found"}, 404

        try:
            new_place = facade.create_place(place_data)
        except (ValueError, TypeError) as e:
            return {
                "error": "Invalid input data",
                "details": str(e)
            }, 400

        return place_to_dict(new_place), 201

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                "id": p.id,
                "title": p.title,
                'price': p.price,
                "latitude": p.latitude,
                "longitude": p.longitude
            }
            for p in places
        ], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place_to_dict(place), 200

    @api.expect(place_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place not found")
    @api.response(404, "Owner not found")
    def put(self, place_id):
        """Update a place's information"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        place_data = api.payload

        # Validate owner exists if provided
        if "owner_id" in place_data:
            owner = facade.get_user(place_data["owner_id"])
            if not owner:
                return {"error": "Owner not found"}, 404

        try:
            updated = facade.update_place(place_id, place_data)
        except (ValueError, TypeError) as e:
            return {"error": "Invalid input data", "details": str(e)}, 400

        return place_to_dict(updated), 200


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        try:
            reviews = facade.get_reviews_by_place(place_id)
        except (ValueError, TypeError) as e:
            return {"error": "Invalid input data", "details": str(e)}, 400

        return [{"id": r.id, "text": r.text, "rating": r.rating} for r in reviews], 200
