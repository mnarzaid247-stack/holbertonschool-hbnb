CREATE DATABASE IF NOT EXISTS hbnb_db;
USE hbnb_db;

DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS place;
DROP TABLE IF EXISTS amenity;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36) NOT NULL,
    CONSTRAINT fk_place_owner
        FOREIGN KEY (owner_id) REFERENCES user(id)
        ON DELETE CASCADE
);

CREATE TABLE review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    CONSTRAINT chk_review_rating CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT fk_review_user
        FOREIGN KEY (user_id) REFERENCES user(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_place
        FOREIGN KEY (place_id) REFERENCES place(id)
        ON DELETE CASCADE,
    CONSTRAINT uq_user_place UNIQUE (user_id, place_id)
);

CREATE TABLE amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    CONSTRAINT fk_place_amenity_place
        FOREIGN KEY (place_id) REFERENCES place(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_place_amenity_amenity
        FOREIGN KEY (amenity_id) REFERENCES amenity(id)
        ON DELETE CASCADE
);
