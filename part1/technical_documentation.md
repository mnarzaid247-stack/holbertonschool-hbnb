1- User regestration: POST/users
sequenceDiagram
autonumber
participant Client as User/Client
participant API as Presentation(API Controller)
participant Facade as Business(HBnBFacade)
participant UserModel as Business(User Model)
participant UserRepo as Persistence(User Repository)
participant DB as Database

Client->>API: POST /users {first_name,last_name,email,password}
API->>API: Validate request body (required fields, email format)
API->>Facade: register_user(dto)

Facade->>UserRepo: find_by_email(dto.email)
UserRepo->>DB: SELECT user WHERE email=...
DB-->>UserRepo: user? (found/none)
UserRepo-->>Facade: user? (found/none)

alt Email already exists
Facade-->>API: 409 Conflict (email already in use)
API-->>Client: 409 + error message
else New email
Facade->>UserModel: set_password(dto.password) (hash)
Facade->>UserRepo: create(user_data)
UserRepo->>DB: INSERT INTO users(...)
DB-->>UserRepo: created user_id
UserRepo-->>Facade: created user
Facade-->>API: 201 Created + user payload (no password)
API-->>Client: 201 Created
end
(layer flow goes here)

2-Place creation :POST/place 
sequenceDiagram
autonumber
participant Client as User/Client
participant API as Presentation(API Controller)
participant Auth as Presentation(Auth Middleware)
participant Facade as Business(HBnBFacade)
participant PlaceModel as Business(Place Model)
participant PlaceRepo as Persistence(Place Repository)
participant DB as Database

Client->>API: POST /places (Bearer token) {title,description,price,latitude,longitude,amenity_ids?}
API->>Auth: verify_token(token)
Auth-->>API: user_id (or auth error)

alt Invalid/expired token
API-->>Client: 401 Unauthorized
else Auth OK
API->>API: Validate request body (types, required fields)
API->>Facade: create_place(user_id, dto)

Facade->>Facade: Apply business rules (price>=0, valid lat/lon)
Facade->>PlaceModel: create entity (owner=user_id)
Facade->>PlaceRepo: create(place_data)
PlaceRepo->>DB: INSERT INTO places(...)
DB-->>PlaceRepo: created place_id
PlaceRepo-->>Facade: created place
Facade-->>API: 201 Created + place payload
API-->>Client: 201 Created
end
(layer flow goes here)

4) Fetch Places List — GET /places?filters
sequenceDiagram
autonumber
participant Client as User/Client
participant API as Presentation(API Controller)
participant Facade as Business(HBnBFacade)
participant PlaceRepo as Persistence(Place Repository)
participant DB as Database

Client->>API: GET /places?min_price=100&max_price=500&lat=24.7&lon=46.7&page=1&limit=20
API->>API: Validate query params (types, ranges, defaults)
API->>Facade: list_places(filters, pagination)

Facade->>Facade: Normalize filters (defaults, bounds)
Facade->>PlaceRepo: search(filters, pagination)
PlaceRepo->>DB: SELECT ... FROM places WHERE ... LIMIT/OFFSET ...
DB-->>PlaceRepo: places[]
PlaceRepo-->>Facade: places[]
Facade-->>API: 200 OK + places[] (+ pagination meta)
API-->>Client: 200 OK + response body
