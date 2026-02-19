#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text": fields.String(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
})

review_update_model = api.model("ReviewUpdate", {
    "text": fields.String,
})

@api.route("/")
class ReviewList(Resource):
    def get(self):
        reviews = facade.get_all_reviews()
        return [facade.serialize_review(r) for r in reviews], 200

    @api.expect(review_model, validate=True)
    def post(self):
        try:
            r = facade.create_review(api.payload)
            return facade.serialize_review(r), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except LookupError as e:
            return {"error": str(e)}, 404

@api.route("/<review_id>")
class ReviewResource(Resource):
    def get(self, review_id):
        r = facade.get_review(review_id)
        if not r:
            return {"error": "Review not found"}, 404
        return facade.serialize_review(r), 200

    @api.expect(review_update_model, validate=True)
    def put(self, review_id):
        try:
            updated = facade.update_review(review_id, api.payload)
            if not updated:
                return {"error": "Review not found"}, 404
            return facade.serialize_review(updated), 200
        except ValueError as e:
            return {"error": str(e)}, 400

    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404
        return {"status": "deleted"}, 200
