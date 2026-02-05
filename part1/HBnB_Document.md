## API Interaction Flow

This section describes how API requests are processed in the HBnB system.
It illustrates the interaction between the Presentation layer, the Business Logic layer,
and the Persistence layer using sequence diagrams.

Each sequence diagram shows how a client request is validated, routed through
the HBnBFacade, processed according to business rules, and persisted using
repository abstractions. The goal is to clearly demonstrate responsibility
separation and request flow consistency across different API endpoints.


## 1) User Registration — POST /users

```mermaid
sequenceDiagram
autonumber
participant Client as User/Client
participant API as API Controller
participant Facade as HBnBFacade
participant UserRepo as User Repository
participant DB as Database

Client->>API: POST /users
API->>API: Validate request body
API->>Facade: register_user()

Facade->>UserRepo: find_by_email()
UserRepo->>DB: SELECT user
DB-->>UserRepo: result
UserRepo-->>Facade: result

alt Email exists
Facade-->>API: 409 Conflict
API-->>Client: Error
else Email not found
Facade->>UserRepo: create(user)
UserRepo->>DB: INSERT user
DB-->>UserRepo: created id
UserRepo-->>Facade: success
Facade-->>API: 201 Created
API-->>Client: Success
end
```

---


### User Registration Flow — Explanation

**Purpose**
This flow handles the creation of a new user account while ensuring data validity
and email uniqueness.

**Layer Responsibilities**
- The API Controller validates request format and required fields.
- The HBnBFacade coordinates the registration logic.
- The User Repository handles data lookup and persistence.
- The Database stores the user record.

**Business Rules Applied**
- Email addresses must be unique.
- Required fields must be provided.
- Data must follow expected formats before reaching the business layer.

**Flow Summary**
1. The client sends a registration request.
2. The controller validates the request structure.
3. The facade checks if the email already exists.
4. If the email exists, the process stops with a conflict response.
5. Otherwise, the new user is saved.
6. A success response is returned.

**Error Scenarios**
- Invalid request format → 400 Bad Request
- Email already exists → 409 Conflict
- Database failure → 500 Internal Server Error


## 2) Place Creation — POST /places

```mermaid
sequenceDiagram
autonumber
participant Client as User
participant API as API Controller
participant Auth as Auth Middleware
participant Facade as HBnBFacade
participant PlaceRepo as Place Repository
participant DB as Database

Client->>API: POST /places
API->>Auth: verify_token()
Auth-->>API: user_id

alt Invalid token
API-->>Client: 401 Unauthorized
else Valid token
API->>Facade: create_place()
Facade->>PlaceRepo: save(place)
PlaceRepo->>DB: INSERT place
DB-->>PlaceRepo: created id
PlaceRepo-->>Facade: success
Facade-->>API: 201 Created
API-->>Client: Success
end
```

---

### Place Creation Flow — Explanation

**Purpose**
This flow allows an authenticated user to create a new place listing.

**Layer Responsibilities**
- The API Controller receives the request and delegates authentication.
- Auth Middleware validates the token and extracts the user_id.
- The HBnBFacade applies business rules and orchestrates creation.
- The Place Repository persists the place.
- The Database stores the place record.

**Business Rules Applied**
- Only authenticated users can create a place.
- The owner of the place is derived from the token (`user_id`), not trusted from the request body.
- Place fields must pass validation (e.g., required fields, non-empty values, valid price/range if defined).

**Flow Summary**
1. Client sends POST /places.
2. Controller calls auth middleware to verify the token.
3. If invalid → request stops with 401.
4. If valid → facade creates the place using the authenticated user_id.
5. Repository saves the place to the database.
6. Success response is returned.

**Error Scenarios**
- Missing/invalid token → 401 Unauthorized
- Invalid request data → 400 Bad Request
- Database failure → 500 Internal Server Error


## 3) Review Submission — POST /reviews

```mermaid
sequenceDiagram
autonumber
participant Client as User
participant API as API Controller
participant Auth as Auth Middleware
participant Facade as HBnBFacade
participant PlaceRepo as Place Repository
participant ReviewRepo as Review Repository
participant DB as Database

Client->>API: POST /reviews
API->>Auth: verify_token()
Auth-->>API: user_id

alt Invalid token
API-->>Client: 401 Unauthorized
else Valid token
API->>Facade: submit_review()
Facade->>PlaceRepo: find_place()
PlaceRepo->>DB: SELECT place
DB-->>PlaceRepo: result
PlaceRepo-->>Facade: result

alt Place not found
Facade-->>API: 404 Not Found
API-->>Client: Error
else Place exists
Facade->>ReviewRepo: save(review)
ReviewRepo->>DB: INSERT review
DB-->>ReviewRepo: created id
ReviewRepo-->>Facade: success
Facade-->>API: 201 Created
API-->>Client: Success
end
end
```

---


### Review Submission Flow — Explanation

**Purpose**
This flow allows an authenticated user to submit a review for an existing place.

**Layer Responsibilities**
- The API Controller receives the request and delegates authentication.
- Auth Middleware validates the token and extracts the user_id.
- The HBnBFacade ensures the place exists and applies review rules.
- The Place Repository is used to verify the target place.
- The Review Repository persists the review.
- The Database stores the review record.

**Business Rules Applied**
- User must be authenticated.
- The place must exist before creating a review.
- Review fields must be valid (e.g., rating range, required text if defined).
- The reviewer identity comes from the token (`user_id`), not trusted from the request body.

**Flow Summary**
1. Client sends POST /reviews.
2. Token is verified; invalid token stops the request with 401.
3. Facade checks that the referenced place exists.
4. If the place does not exist → return 404.
5. If it exists → repository saves the new review.
6. Success response is returned.

**Error Scenarios**
- Missing/invalid token → 401 Unauthorized
- Place not found → 404 Not Found
- Invalid review data → 400 Bad Request
- Database failure → 500 Internal Server Error



## 4) Fetch Places — GET /places

```mermaid
sequenceDiagram
autonumber
participant Client as User
participant API as API Controller
participant Facade as HBnBFacade
participant PlaceRepo as Place Repository
participant DB as Database

Client->>API: GET /places
API->>Facade: list_places()
Facade->>PlaceRepo: search()
PlaceRepo->>DB: SELECT places
DB-->>PlaceRepo: results
PlaceRepo-->>Facade: results
Facade-->>API: 200 OK
API-->>Client: Return places
```

### Fetch Places Flow — Explanation

**Purpose**
This flow retrieves a list of places from the system.

**Layer Responsibilities**
- The API Controller receives the request and calls the facade.
- The HBnBFacade coordinates retrieval logic.
- The Place Repository performs the query.
- The Database returns matching place records.

**Business Rules Applied**
- This endpoint is typically read-only and may be public (no auth) unless specified otherwise.
- Optional filtering/pagination can be applied at the repository level if implemented.

**Flow Summary**
1. Client sends GET /places.
2. Controller calls list_places() on the facade.
3. Facade requests results from the repository.
4. Repository queries the database and returns results.
5. Controller returns the list with 200 OK.

**Error Scenarios**
- Database failure → 500 Internal Server Error


### Notes on Layer Separation

In all flows, the Presentation layer does not directly access the database.
All business decisions are centralized in the HBnBFacade, while repositories
encapsulate persistence operations. This separation improves maintainability
and keeps responsibilities clear across the system.
