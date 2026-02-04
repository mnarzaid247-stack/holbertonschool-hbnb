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
