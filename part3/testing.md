# Part 3 Testing Documentation

This file documents the testing performed for Part 3 tasks 1, 2, 7, and 8.

---

## Task 1 - Application Setup and API Documentation

### Run the application
python3 run.py

### Expected result
The Flask application starts successfully without errors.

### Actual result
The application started successfully and the server was running.

### Swagger documentation test

Open this URL in the browser:

http://127.0.0.1:5000/api/v1/

### Expected result
The Swagger API documentation page loads correctly.

### Actual result
The Swagger documentation loaded successfully.

---

## Task 2 - Authentication and JWT Protection

### Create a user
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "1234"
}'

### Expected result
A new user is created successfully.

### Actual result
The user was created successfully.

---

### Login with the created user
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "john@example.com",
  "password": "1234"
}'

### Expected result
A JWT access token is returned.

### Actual result
The login was successful and a JWT token was returned.

---

### Access a protected route
curl -X GET http://127.0.0.1:5000/api/v1/auth/protected \
-H "Authorization: Bearer YOUR_TOKEN_HERE"

### Expected result
The protected route is accessible only with a valid JWT token.

### Actual result
The protected route was accessed successfully using the JWT token.

---

## Task 7 - User Model Database Mapping

### Run Python
python3

### Then execute
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="1234"
    )
    db.session.add(user)
    db.session.commit()

    users = User.query.all()
    print(users)

### Expected result
The user is stored and retrieved successfully from the database.

### Actual result
The user was inserted and retrieved successfully.

---

## Task 8 - Place, Review, and Amenity Model Database Mapping

### Run Python
python3

### Then execute
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

app = create_app()

with app.app_context():
    user = User(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        password="1234"
    )
    db.session.add(user)
    db.session.commit()

    place = Place(
        title="Test Place",
        description="Nice place",
        price=100,
        latitude=24.7136,
        longitude=46.6753,
        owner_id=user.id
    )
    db.session.add(place)

    amenity = Amenity(name="WiFi")
    db.session.add(amenity)
    db.session.commit()

    review = Review(
        text="Great place",
        rating=5,
        user_id=user.id,
        place_id=place.id
    )
    db.session.add(review)
    db.session.commit()

    print(Place.query.all())
    print(Amenity.query.all())
    print(Review.query.all())

### Expected result
All models are stored and retrieved successfully.

### Actual result
All models were inserted and retrieved successfully.

---

## Notes

- Replace YOUR_TOKEN_HERE with the real JWT token.
- All tests were executed successfully.
