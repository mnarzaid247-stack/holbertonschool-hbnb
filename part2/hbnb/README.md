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
| **Business Logic** | Rules and validation for our data | "Email must be valid," "Price > 0" |
| **Facade** | Middle person between API and storage | Asks repository to save a user |
| **Persistence** | Stores and retrieves data | In-memory dict (later: database) |

---

## Getting Started

### What You Need

- Python 3.8 or newer
- pip (comes with Python)

### Setup

```bash
# Get the code
git clone <your-repo-url>
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

Instead of the API layer directly talking to the repository, we use a `Facade` class. It's like having a receptionist who handles all the requests instead of everyone walking into the office randomly. This keeps everything clean and organized.

### Repository Pattern

The `repository.py` file handles all data storage. Right now it's in-memory (just Python dicts), but later we can swap it out for a real database without changing the rest of the code.

### Models with Validation

Each model (User, Place, etc.) can validate its own data. A User knows what makes a valid email. A Place knows its price should be positive. This keeps validation rules close to the data.

---

## What We're Building

This is educational code, not production software. We're learning good practices by building a simplified AirBnB-like API. Later parts will add a database, more complex features, and real testing practices.

---

## Authors

- Aljawharah
- Manar
- Reem

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

## Roadmap

- [x] **Part 1** — Project structure, in-memory repository, Facade skeleton
- [ ] **Part 2** — API endpoints for Users, Places, Reviews, Amenities
- [ ] **Part 3** — SQLAlchemy persistence layer replacing in-memory repo
- [ ] **Part 4** — Authentication and authorization

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
- [Facade Design Pattern](https://refactoring.guru/design-patterns/facade/python/example)
- [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
