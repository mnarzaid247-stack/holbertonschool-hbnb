# HBnB Part 3 - ER Diagram

## Description
This diagram represents the database structure for the HBnB application in Part 3, including all entities and their relationships.

## Diagram

```mermaid
erDiagram
    user {
        string id
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    place {
        string id
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id
    }

    review {
        string id
        string text
        int rating
        string user_id
        string place_id
    }

    amenity {
        string id
        string name
    }

    place_amenity {
        string place_id
        string amenity_id
    }

    user ||--o{ place : owns
    user ||--o{ review : writes
    place ||--o{ review : receives
    place ||--o{ place_amenity : has
    amenity ||--o{ place_amenity : includes
