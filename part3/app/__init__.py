from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt 
from flask_jwt_extended import JWTManager
from app.api.v1.auth import api as auth_ns

bcrypt = Bcrypt()
jwt = JWTManager()
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from flask import jsonify

    @jwt.unauthorized_loader
    def unauthorized_callback(err_str):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(err_str):
        return jsonify({"error": "Invalid token"}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired"}), 401
        
    api = Api(
            app,
            version='1.0',
            title='HBnB API',
            description='HBnB Application API',
            doc='/api/v1/'
        )
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1")
    return app
