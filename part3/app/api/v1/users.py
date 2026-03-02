#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True, description="First name of the user"),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="User password"),
    },
)


@api.route("/")
class UserList(Resource):

    @api.response(200, "Users retrieved successfully")
    @jwt_required()
    def get(self):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            return {"error": "Missing Authorization Header"}, 401
        users = facade.get_all_users()
        return [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
            }
            for u in users
        ], 200

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data or email already registered")
    def post(self):
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            return {"error": "Invalid input data", "details": str(e)}, 400

        return {
            "id": new_user.id,
            "message": "User successfully created"
        }, 201


@api.route("/<user_id>")
class UserResource(Resource):

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, "User updated successfully")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input data")
    def put(self, user_id):
        user_data = api.payload

        try:
            updated = facade.update_user(user_id, user_data)
        except (ValueError, TypeError) as e:
            return {"error": "Invalid input data", "details": str(e)}, 400

        if not updated:
            return {"error": "User not found"}, 404

        return {
            "id": updated.id,
            "first_name": updated.first_name,
            "last_name": updated.last_name,
            "email": updated.email,
        }, 200
