#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String(required=True),
    "amenity_ids": fields.List(fields.String),
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "amenity_ids": fields.List(fields.String),
})

@api.route("/")
class PlaceList(Resource):
    def get(self):
        places = facade.get_all_places()
        return [facade.serialize_place(p) for p in places], 200

    @api.expect(place_model, validate=True)
    def post(self):
        try:
            p = facade.create_place(api.payload)
            return facade.serialize_place(p), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except LookupError as e:
            return {"error": str(e)}, 404

@api.route("/<place_id>")
class PlaceResource(Resource):
    def get(self, place_id):
        p = facade.get_place(place_id)
        if not p:
            return {"error": "Place not found"}, 404
        return facade.serialize_place(p), 200

    @api.expect(place_update_model, validate=True)
    def put(self, place_id):
        try:
            updated = facade.update_place(place_id, api.payload)
            if not updated:
                return {"error": "Place not found"}, 404
            return facade.serialize_place(updated), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except LookupError as e:
            return {"error": str(e)}, 404

@api.route("/<place_id>/reviews")
class PlaceReviews(Resource):
    def get(self, place_id):
        p = facade.get_place(place_id)
        if not p:
            return {"error": "Place not found"}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [facade.serialize_review(r) for r in reviews], 200
