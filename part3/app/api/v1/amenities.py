#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(required=True, description="Name of the amenity"),
        "description": fields.String(description="Description of the amenity"),
    },
)


@api.route("/")
class AmenityList(Resource):
    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        amenities = facade.get_all_amenities()
        return [
            {"id": a.id, "name": a.name, "description": a.description}
            for a in amenities
        ], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin:
            return {"error": "Admin privileges required"}, 403

        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {
            "id": new_amenity.id,
            "name": new_amenity.name,
            "description": new_amenity.description,
        }, 201


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {
            "id": amenity.id,
            "name": amenity.name,
            "description": amenity.description,
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    @api.response(401, "Authentication required")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def put(self, amenity_id):
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin:
            return {"error": "Admin privileges required"}, 403

        amenity_data = api.payload
        updated = facade.update_amenity(amenity_id, amenity_data)
        if not updated:
            return {"error": "Amenity not found"}, 404

        return {
            "id": updated.id,
            "name": updated.name,
            "description": updated.description,
        }, 200
