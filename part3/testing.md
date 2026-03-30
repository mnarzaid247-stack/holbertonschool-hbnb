# Testing Documentation - Part 3

## Task 1: Password Hashing

### Objective
Ensure that passwords are securely hashed, not exposed in API responses, and validated correctly.

### Test 1: Create user with password

Request:

    curl -X POST http://127.0.0.1:5000/api/v1/users/ \
    -H "Content-Type: application/json" \
    -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"1234"}'

Expected Result:
- Status code: 201 Created
- User is created successfully
- Password is not included in the response

### Test 2: Verify password is hashed

Verification:
- Check the database directly
- Password is not stored as "1234"
- Stored password appears as a bcrypt hash

### Test 3: Verify password validation

Verification:
- Correct password returns True
- Incorrect password returns False

### Result
Passwords are securely hashed, not exposed in API responses, and validated correctly.

---

## Task 2: JWT Authentication

### Objective
Verify that users can log in, receive a JWT token, and access protected endpoints using that token.

### Test 1: Login with valid credentials

Request:

    curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"john@example.com","password":"1234"}'

Expected Result:
- Status code: 200 OK
- JWT access token is returned

### Test 2: Login with invalid password

Request:

    curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"john@example.com","password":"wrongpassword"}'

Expected Result:
- Status code: 401 Unauthorized
- Error message is returned

### Test 3: Access protected endpoint with token

Request:

    curl -X GET http://127.0.0.1:5000/api/v1/auth/protected \
    -H "Authorization: Bearer <TOKEN>"

Expected Result:
- Status code: 200 OK
- Access is granted

### Test 4: Access protected endpoint without token

Request:

    curl -X GET http://127.0.0.1:5000/api/v1/auth/protected

Expected Result:
- Status code: 401 Unauthorized
- Missing token error is returned

### Result
JWT authentication works correctly. Users can log in and access protected routes only with a valid token.

---

## Task 3: Authorization and Review Validation

### Objective
Verify ownership validation, self-review restriction, and duplicate review prevention.

### Test 1: Prevent reviewing own place

Steps:
- Create a user
- Create a place owned by that user
- Attempt to create a review for that same place using the same user

Expected Result:
- Request is rejected
- Error message is returned

### Test 2: Prevent duplicate review

Steps:
- Create a user
- Create a place
- Submit one review successfully
- Attempt to submit a second review for the same place using the same user

Expected Result:
- Second request is rejected
- Duplicate review is not allowed

### Test 3: Ownership validation on update

Steps:
- User A creates a review
- User B attempts to update User A's review

Expected Result:
- Status code: 403 Forbidden
- Update is rejected

### Test 4: Ownership validation on delete

Steps:
- User A creates a review
- User B attempts to delete User A's review

Expected Result:
- Status code: 403 Forbidden
- Delete is rejected

### Result
Authorization rules for reviews work correctly. Users cannot review their own place, cannot submit duplicate reviews, and cannot modify or delete reviews they do not own.

---

## Task 7: User Model Database Mapping

### Objective
Verify that the User model is correctly mapped to the database table.

### Test

Run Python:

    python3

Then execute:

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

Expected Result:
- User is inserted into the database
- User is retrieved successfully from the database

### Actual Result
The user was inserted and retrieved successfully.

### Result
User model mapping works correctly.

---

## Task 8: Repository Layer Testing

### Objective
Verify that the repository layer works correctly with database persistence instead of in-memory storage.

### Setup
- Database created using schema.sql
- Seed data inserted using seed.sql
- Application configured with SQLAlchemy repositories

### Test 1: Create and retrieve user

Steps:
- Create a user through the API
- Retrieve all users using GET /api/v1/users/

Expected Result:
- User is stored in the database
- User appears in the returned list

### Test 2: Update user

Steps:
- Update user data through PUT /api/v1/users/<user_id>

Expected Result:
- Updated values are saved in the database
- Retrieving the same user shows updated data

### Test 3: Create and retrieve amenity

Steps:
- Create an amenity through the API
- Retrieve all amenities using GET /api/v1/amenities/

Expected Result:
- Amenity is stored successfully
- Amenity appears in the returned list

### Test 4: Create place

Steps:
- Create a place linked to an existing user

Expected Result:
- Place is stored successfully
- owner_id is saved correctly in the database

### Test 5: Create review

Steps:
- Create a review linked to an existing user and place

Expected Result:
- Review is stored successfully
- user_id and place_id relationships are correct

### Test 6: Verify relationships directly in database

Queries used:

    SELECT * FROM user;
    SELECT * FROM place;
    SELECT * FROM review;
    SELECT * FROM place_amenity;

Expected Result:
- Records exist in the correct tables
- Relationships between users, places, reviews, and amenities are correct

### Result
The repository layer correctly handles create, read, and update operations with database persistence and maintains the expected relationships.

---

## Final Result

All required Part 3 features were tested successfully:
- Password hashing
- JWT authentication
- Authorization and review validation
- User model database mapping
- Repository layer with database persistence

The application works correctly with secure authentication, proper authorization, and database-backed storage.
