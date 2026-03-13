#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(required=True, description="Rating of the place (1-5)"),
        "user_id": fields.String(required=True, description="ID of the user"),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    @api.response(404, "Place not found")
    @jwt_required()
    def post(self):
        claims = get_jwt()
        user_id = claims.get("id")
        is_admin = claims.get("is_admin", False)

        review_data = api.payload

        if not is_admin and review_data["user_id"] != user_id:
            return {"error": "Unauthorized action"}, 403

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {"error": "Invalid input data", "details": str(e)}, 400

        return {
            "id": new_review.id,
            "text": new_review.text,
            "rating": new_review.rating,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id,
        }, 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        reviews = facade.get_all_reviews()
        return [{"id": r.id, "text": r.text, "rating": r.rating} for r in reviews], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def put(self, review_id):
        claims = get_jwt()
        user_id = claims.get("id")
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        review_data = api.payload

        try:
            updated = facade.update_review(review_id, review_data)
        except ValueError as e:
            return {"error": "Invalid input data", "details": str(e)}, 400

        return {
            "id": updated.id,
            "text": updated.text,
            "rating": updated.rating,
            "user_id": updated.user_id,
            "place_id": updated.place_id,
        }, 200

    @api.response(200, "Review deleted successfully")
    @api.response(401, "Authentication required")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        claims = get_jwt()
        user_id = claims.get("id")
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200