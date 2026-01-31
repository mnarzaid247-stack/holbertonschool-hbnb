## High-Level Package Diagram (Text-Based)

+-----------------------------------------------------------+
| Presentation Layer (Services / API)                        |
|-----------------------------------------------------------|
| - API Controllers / Routes                                 |
| - Request/Response handling                                |
+---------------------------+-------------------------------+
                            |
                            | calls
                            v
+-----------------------------------------------------------+
| Facade (HBnBFacade)                                        |
|-----------------------------------------------------------|
| - Unified interface for the API layer                      |
| - Delegates operations to the correct service              |
|   (User / Place / Review / Amenity)                        |
+---------------------------+-------------------------------+
                            |
                            | delegates
                            v
+-----------------------------------------------------------+
| Business Logic Layer (Models / Core)                       |
|-----------------------------------------------------------|
| Domain Models:                                              |
| - User(first_name, last_name, email, password, is_admin)   |
| - Place(title, description, price, latitude, longitude)    |
| - Review(rating, comment, user_id, place_id)               |
| - Amenity(name, description)                               |
|                                                           |
| Services / Managers:                                       |
| - UserService, PlaceService, ReviewService, AmenityService |
+---------------------------+-------------------------------+
                            |
                            | CRUD / queries
                            v
+-----------------------------------------------------------+
| Persistence Layer (Storage)                                |
|-----------------------------------------------------------|
| - Repositories / DAO                                       |
|   UserRepository, PlaceRepository, ReviewRepository,       |
|   AmenityRepository                                        |
| - Database (implemented later in Part 3)                   |
+-----------------------------------------------------------+

## Notes (Responsibilities)

- Presentation Layer:
  Receives HTTP requests and returns responses. It does not implement business rules.
  It only calls HBnBFacade.

- Facade (HBnBFacade):
  A single entry point for the Presentation layer. It routes each action to the
  correct service in the Business Logic layer.

- Business Logic Layer:
  Implements rules and validation for the core entities (User, Place, Review, Amenity).
  It decides what must be saved or fetched and calls repositories to do it.

- Persistence Layer:
  Handles storage and retrieval through repositories/DAO. It hides database details
  from the business logic.

## Data Flow

Client → API/Controllers → HBnBFacade → Services/Models → Repositories/DB → back to Client
