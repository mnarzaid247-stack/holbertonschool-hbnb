# HBnB - AirBnB Clone

A RESTful API application built with Flask and Flask-RESTx, structured around clean separation of concerns across Presentation, Business Logic, and Persistence layers.

---

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py     # User endpoints
│   │       ├── places.py    # Place endpoints
│   │       ├── reviews.py   # Review endpoints
│   │       └── amenities.py # Amenity endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User business logic
│   │   ├── place.py         # Place business logic
│   │   ├── review.py        # Review business logic
│   │   └── amenity.py       # Amenity business logic
│   ├── services/
│   │   ├── __init__.py      # Facade singleton
│   │   └── facade.py        # HBnBFacade — inter-layer communication
│   └── persistence/
│       ├── __init__.py
│       └── repository.py    # Abstract repo + InMemoryRepository
├── run.py                   # Application entry point
├── config.py                # Environment configuration
├── requirements.txt         # Python dependencies
└── README.md
```

### Layer Overview

| Layer | Location | Responsibility |
|---|---|---|
| **Presentation** | `app/api/` | API endpoints and request/response handling |
| **Business Logic** | `app/models/` | Core entities and validation rules |
| **Service / Facade** | `app/services/` | Orchestrates interaction between layers |
| **Persistence** | `app/persistence/` | Object storage (in-memory now, DB later) |

---

## Key Design Patterns

### Facade Pattern
The `HBnBFacade` class (`app/services/facade.py`) acts as a single point of contact between the API layer and the underlying repositories. A singleton instance is created in `app/services/__init__.py` and shared across the app.

### Repository Pattern
`repository.py` defines an abstract `Repository` interface and a concrete `InMemoryRepository` implementation. This makes it easy to swap in a database-backed repository (SQLAlchemy) in Part 3 without changing any business logic.

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd hbnb

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python run.py
```

The app will start in debug mode. Visit `http://127.0.0.1:5000/api/v1/` to access the Swagger UI (no routes are active yet at this stage).

---

## Configuration

Environment-specific settings live in `config.py`. The default config uses `DevelopmentConfig` which enables debug mode. You can extend this file with database URIs and other settings as the project grows.

```python
# Override the secret key via environment variable
export SECRET_KEY="your-secret-key"
```

---

## Dependencies

| Package | Purpose |
|---|---|
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
