# HBnB - Part 2: Building the REST API

This is Part 2 of the HBnB (Holberton AirBnB Clone) project. Here, we're building a REST API using Flask and Flask-RESTx, with a focus on clean architecture and separating concerns into different layers.

---

## What We're Learning

This part of the project teaches us:

- **Modular Design**: How to structure a Python app so it doesn't become a giant mess of code. Each layer has a specific job.
- **REST API Development**: Building endpoints with Flask-RESTx, handling requests and responses, and making sure the API documentation is clean.
- **Business Logic**: Implementing the core "rules" of our app—like what makes a valid user or review.
- **Data Handling**: Working with nested objects and returning complex data structures from our API endpoints.
- **Testing**: Making sure our endpoints actually work and handle weird requests gracefully.

---

## How It's Organized

The project is split into **layers**. Think of it like a restaurant: the customer (API client) places an order with the waiter (API), the waiter tells the kitchen (business logic) what to make, and the kitchen stores ingredients in the pantry (persistence).

```text
hbnb/
├── app/
│   ├── __init__.py              # Sets up the Flask app
│   ├── api/
│   │   └── v1/                  # API version 1
│   │       ├── users.py         # User endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       └── amenities.py     # Amenity endpoints
│   ├── models/
│   │   ├── base_model.py        # Base class for all models
│   │   ├── user.py              # User class with validation
│   │   ├── place.py             # Place class
│   │   ├── review.py            # Review class
│   │   └── amenity.py           # Amenity class
│   ├── services/
│   │   └── facade.py            # Facade pattern—talks to repos and models
│   └── persistence/
│       └── repository.py        # Where data actually lives (memory for now)
├── run.py                       # Start the app here
├── config.py                    # Settings (debug mode, secret key, etc.)
├── requirements.txt             # What libraries we need
└── README.md
```

### The Layers Explained

| Layer | Purpose | Example |
| --- | --- | --- |
| **API** | Takes requests, returns JSON responses | `GET /api/v1/users` |
| **Business Logic** | Rules and validation for our data | User validates email format, Place validates price > 0 |
| **Facade** | Single point of contact for all operations | `HBnBFacade` manages all CRUD operations |
| **Persistence** | Stores and retrieves data | `InMemoryRepository` using Python dicts |

---

## Getting Started

### What You Need

- Python 3.8 or newer
- pip (comes with Python)

### Setup

```bash
# Get the code
git clone git@github.com:mnarzaid247-stack/holbertonschool-hbnb.git
cd part2/hbnb

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running It

```bash
python run.py
```

The app starts at `http://127.0.0.1:5000`. Open your browser and check it out! Flask-RESTx provides a nice interface to test your endpoints.

---

## Key Ideas We're Using

### Facade Pattern

The `HBnBFacade` class is the central hub for all business operations. Instead of the API layer directly touching repositories or models, it talks to the facade. The facade handles method calls like `create_user()`, `get_all_places()`, `add_review()`, etc. This keeps the API layer simple and keeps all the complexity hidden.

### Repository Pattern

The `InMemoryRepository` is an abstract repository that stores objects in a Python dictionary. It has methods like `add()`, `get()`, `get_all()`, `update()`, and `delete()`. The key idea is that the Facade doesn't care if data is in memory, a database, or even a spreadsheet—it just calls the same methods. In Part 3, we'll swap this with a SQLAlchemy repository without changing any other code.

### Models with Validation

Each model (User, Place, Amenity, Review) inherits from `BaseModel`, which provides `id`, `created_at`, and `updated_at`. Each model also has its own validation logic:

- **User**: Validates non-empty names and proper email format
- **Place**: Validates title, positive price, and latitude/longitude bounds
- **Amenity**: Validates non-empty name with length limit
- **Review**: Validates non-empty text and rating between 1-5

---

## What We're Building

This is educational code, not production software. We're learning good practices by building a simplified AirBnB-like API. Here's what we have so far:

- **4 Core Models**: User, Place, Amenity, Review—each with validation
- **4 API Endpoints**: `/api/v1/users`, `/api/v1/places`, `/api/v1/amenities`, `/api/v1/reviews`
- **Facade System**: `HBnBFacade` coordinates all operations across repositories and models
- **In-Memory Storage**: Everything is stored in Python dicts for now

Later parts will add a database, more complex relationships, and proper authentication.



## Dependencies

| Package | Purpose |
| --- | --- |
| `flask` | Web framework |
| `flask-restx` | REST API + Swagger UI |

Install with:

```bash
pip install -r requirements.txt
```


---

## Quick API Overview

### Users (`/api/v1/users`)

```bash
# Get all users
GET /api/v1/users

# Create a user
POST /api/v1/users
# Body: { "first_name": "John", "last_name": "Doe", "email": "john@example.com" }

# Get a specific user
GET /api/v1/users/{user_id}
```

### Places (`/api/v1/places`)

```bash
# Get all places
GET /api/v1/places

# Create a place
POST /api/v1/places
# Body: { "title": "Cozy Apartment", "price": 100.0, "owner_id": "user-id", ... }

# Get a specific place
GET /api/v1/places/{place_id}
```

### Amenities (`/api/v1/amenities`)

```bash
# Get all amenities
GET /api/v1/amenities

# Create an amenity
POST /api/v1/amenities
# Body: { "name": "WiFi" }
```

### Reviews (`/api/v1/reviews`)

```bash
# Get all reviews
GET /api/v1/reviews

# Create a review
POST /api/v1/reviews
# Body: { "text": "Great place!", "user_id": "user-id", "place_id": "place-id", "rating": 5 }
```

Visit `http://127.0.0.1:5000/api/v1/` for the interactive Swagger UI where you can test endpoints in your browser!

---

# Testing and Validation Report

## Running the Application

export PYTHONPATH=.
python3 run.py

Swagger documentation available at:
http://127.0.0.1:5000/api/v1/

---

## Running Automated Tests

python3 -m unittest discover -s tests -t . -v

Total tests executed: 10  
All tests passed successfully.

Automated tests cover:

- Model validation (User, Place, Amenity, Review)
- API endpoint testing (Users)
- Success and failure scenarios
- Boundary and invalid input handling

---

## Black-Box Testing Using cURL

The following tests were performed using cURL to verify endpoint behavior and HTTP status codes.

### 1. Create User — Success Case

curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com"}'

Expected Status: 201 Created  
Actual Status: 201 Created  

---

### 2. Create User — Invalid Email

curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{"first_name":"","last_name":"","email":"invalid-email"}'

Expected Status: 400 Bad Request  
Actual Status: 400 Bad Request  

Validation correctly rejected empty fields and invalid email format.

---

### 3. Create User — Duplicate Email

curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{"first_name":"A","last_name":"B","email":"dup@example.com"}'

Second request using same email returns:

Expected Status: 400 Bad Request  
Actual Status: 400 Bad Request  

System correctly prevents duplicate email registration.

---

### 4. Get User — Not Found

curl -i "http://127.0.0.1:5000/api/v1/users/does-not-exist"

Expected Status: 404 Not Found  
Actual Status: 404 Not Found  

---

## Boundary and Edge Case Testing

### User Model
- Empty first_name → rejected
- Empty last_name → rejected
- Invalid email format → rejected
- Duplicate email → rejected

### Place Model
- Empty title → rejected
- Price ≤ 0 → rejected
- Latitude outside [-90, 90] → rejected
- Longitude outside [-180, 180] → rejected

### Amenity Model
- Empty name → rejected
- Name exceeding length limit → rejected

### Review Model
- Empty text → rejected
- Rating outside valid range → rejected
- Invalid user_id or place_id → rejected

---

## Summary

All endpoints were tested using automated unit tests (unittest), manual black-box testing with cURL, and Swagger UI verification.

The API correctly handles:

- Valid requests
- Invalid input data
- Duplicate entries
- Non-existent resources
- Boundary conditions

All validation rules defined in the Business Logic Layer are enforced and reflected in API responses.

## Roadmap

- [x] **Part 1** — Project structure, in-memory repository, Facade skeleton
- [x] **Part 2** — API endpoints for Users, Places, Reviews, Amenities
- [ ] **Part 3** — SQLAlchemy persistence layer replacing in-memory repo
- [ ] **Part 4** — Authentication and authorization
---

## Authors

- Aljawharah
- Manar
- Reem





