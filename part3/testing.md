# Testing Documentation - Part 3

## Task 1: Password Hashing

### Objective
Verify that user passwords are hashed before storage, are not returned in API responses, and can be validated correctly.

---

### Test 1: Create a new user with password

Request
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"1234"}'

Expected Result
- Status code: 201 Created
- User is created successfully
- Password is not included in the response

Example Response
{
  "id": "generated-id",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}

---

### Test 2: Verify password is hashed

Expected Result
- Password is not "1234"
- Password is stored as a hashed value
- If using bcrypt, it usually starts with something like "$2b$"

---

### Test 3: Verify password validation

Expected Result
- verify_password("1234") returns True
- verify_password("wrongpassword") returns False

---

### Test 4: Create user without password

Request
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"Jane","last_name":"Doe","email":"jane@example.com"}'

Expected Result
- Status code: 400 Bad Request
- Error returned because password is missing

---

### Result
Passwords are hashed correctly, not exposed in API responses, and validated properly.

---


## Task 2: JWT Authentication

### Objective
Verify that users can log in, receive a JWT token, and access protected endpoints using that token.

---

### Test 1: Login with correct credentials

Request
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"john@example.com","password":"1234"}'

Expected Result
- Status code: 200 OK
- A JWT access token is returned

Example Response
{
  "access_token": "your_jwt_token_here"
}

---

### Test 2: Login with wrong password

Request
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"john@example.com","password":"wrongpassword"}'

Expected Result
- Status code: 401 Unauthorized
- Error message indicating invalid credentials

---

### Test 3: Access protected route with token

Request
curl -X GET http://127.0.0.1:5000/api/v1/auth/protected \
-H "Authorization: Bearer your_jwt_token_here"

Expected Result
- Status code: 200 OK
- Access granted message

Example Response
{
  "message": "You are authorized"
}

---

### Test 4: Access protected route without token

Request
curl -X GET http://127.0.0.1:5000/api/v1/auth/protected

Expected Result
- Status code: 401 Unauthorized
- Error indicating missing token

---

### Test 5: Access protected route with invalid token

Request
curl -X GET http://127.0.0.1:5000/api/v1/auth/protected \
-H "Authorization: Bearer invalid_token"

Expected Result
- Status code: 401 Unauthorized
- Error indicating invalid token

---

### Result
JWT authentication works correctly. Users can log in, receive a token, and access protected endpoints only with valid authorization.


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


## Task 8 - Repository Layer Testing

### Objective
Test the repository layer after transitioning from in-memory storage to database-backed persistence using SQLAlchemy.

---

### Setup
- Database created using schema.sql
- Test data inserted using seed.sql
- Application configured with SQLAlchemy
- Repositories used:
  - UserRepository
  - PlaceRepository
  - ReviewRepository
  - AmenityRepository

---

### Test Cases

#### 1. Create User
- Endpoint: POST /api/v1/users/
- Expected: User is saved in the database with a unique ID

#### 2. Get All Users
- Endpoint: GET /api/v1/users/
- Expected: Returns a list of users from the database

#### 3. Get User by ID
- Endpoint: GET /api/v1/users/<user_id>
- Expected: Returns correct user data

#### 4. Update User
- Endpoint: PUT /api/v1/users/<user_id>
- Expected: User data is updated in the database

---

#### 5. Create Amenity
- Endpoint: POST /api/v1/amenities/
- Expected: Amenity is saved in the database

#### 6. Get All Amenities
- Endpoint: GET /api/v1/amenities/
- Expected: Returns all amenities from the database

---

#### 7. Create Place
- Endpoint: POST /api/v1/places/
- Expected: Place is saved with correct owner and attributes

#### 8. Get Place by ID
- Endpoint: GET /api/v1/places/<place_id>
- Expected: Returns correct place with owner and amenities

---

#### 9. Create Review
- Endpoint: POST /api/v1/reviews/
- Expected: Review is stored and linked to user and place

#### 10. Prevent Duplicate Review
- Same user tries to review same place twice
- Expected: Request is rejected

---

### Verification

- Checked database directly using SQL queries
- Verified records are inserted, updated, and retrieved correctly
- Confirmed relationships:
  - User ↔ Place
  - Place ↔ Review
  - Place ↔ Amenity

---

### Result

All repository operations are functioning correctly with the database.
Data persistence is confirmed across all entities.
- Replace YOUR_TOKEN_HERE with the real JWT token.
- All tests were executed successfully.
