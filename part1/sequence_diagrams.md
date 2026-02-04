```mermaid
sequenceDiagram
autonumber
participant Client as User/Client
participant API as API Controller
participant Facade as HBnBFacade
participant UserModel as User Model
participant UserRepo as User Repository
participant DB as Database

Client->>API: POST /users {first_name,last_name,email,password}
API->>API: Validate request body
API->>Facade: register_user(dto)

Facade->>UserRepo: find_by_email(email)
UserRepo->>DB: SELECT user WHERE email=...
DB-->>UserRepo: result
UserRepo-->>Facade: result

alt Email exists
Facade-->>API: 409 Conflict
API-->>Client: Error response
else Email not found
Facade->>UserModel: hash password
Facade->>UserRepo: create(user)
UserRepo->>DB: INSERT user
DB-->>UserRepo: created id
UserRepo-->>Facade: user created
Facade-->>API: 201 Created
API-->>Client: Success response
end
sequenceDiagram
autonumber
participant Client as User/Client
participant API as API Controller
participant Auth as Auth Middleware
participant Facade as HBnBFacade
participant PlaceModel as Place Model
participant PlaceRepo as Place Repository
participant DB as Database

Client->>API: POST /places (token)
API->>Auth: verify_token()
Auth-->>API: user_id

alt Invalid token
API-->>Client: 401 Unauthorized
else Valid token
API->>Facade: create_place(user_id, data)
Facade->>PlaceModel: validate rules
Facade->>PlaceRepo: save(place)
PlaceRepo->>DB: INSERT place
DB-->>PlaceRepo: created id
PlaceRepo-->>Facade: place created
Facade-->>API: 201 Created
API-->>Client: Success response
end
sequenceDiagram
autonumber
participant Client as User/Client
participant API as API Controller
participant Auth as Auth Middleware
participant Facade as HBnBFacade
participant ReviewModel as Review Model
participant PlaceRepo as Place Repository
participant ReviewRepo as Review Repository
participant DB as Database

Client->>API: POST /places/{id}/reviews
API->>Auth: verify_token()
Auth-->>API: user_id

alt Invalid token
API-->>Client: 401 Unauthorized
else Valid token
API->>Facade: submit_review(user_id, place_id, data)
Facade->>PlaceRepo: find place
PlaceRepo->>DB: SELECT place
DB-->>PlaceRepo: result
PlaceRepo-->>Facade: result

alt Place not found
Facade-->>API: 404 Not Found
API-->>Client: Error response
else Place exists
Facade->>ReviewModel: validate rating
Facade->>ReviewRepo: save(review)
ReviewRepo->>DB: INSERT review
DB-->>ReviewRepo: created id
ReviewRepo-->>Facade: review created
Facade-->>API: 201 Created
API-->>Client: Success response
end
end
sequenceDiagram
autonumber
participant Client as User/Client
participant API as API Controller
participant Facade as HBnBFacade
participant PlaceRepo as Place Repository
participant DB as Database

Client->>API: GET /places?filters
API->>API: Validate query params
API->>Facade: list_places(filters)

Facade->>PlaceRepo: search(filters)
PlaceRepo->>DB: SELECT places
DB-->>PlaceRepo: places list
PlaceRepo-->>Facade: places list
Facade-->>API: 200 OK
API-->>Client: Return places
