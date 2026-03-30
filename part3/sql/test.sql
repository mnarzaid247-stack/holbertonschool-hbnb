USE hbnb_db;

-- Check seed data
SELECT * FROM user;
SELECT * FROM amenity;

-- Insert test user
INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
    '8d2f8b7d-3c96-4d72-a8df-9d1e4c7b1a11',
    'John',
    'Doe',
    'john@example.com',
    '$2b$12$anouBdkyvtFYvqSGwotKieQhSyjExdIyKUPQngFxx2G7b7iWy9tau',
    FALSE
);

-- Read user
SELECT * FROM user WHERE id = '8d2f8b7d-3c96-4d72-a8df-9d1e4c7b1a11';

-- Update user
UPDATE user
SET first_name = 'Johnny'
WHERE id = '8d2f8b7d-3c96-4d72-a8df-9d1e4c7b1a11';

SELECT * FROM user WHERE id = '8d2f8b7d-3c96-4d72-a8df-9d1e4c7b1a11';

-- Insert place
INSERT INTO place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222',
    'Nice Apartment',
    'City center',
    250.00,
    24.7136,
    46.6753,
    '8d2f8b7d-3c96-4d72-a8df-9d1e4c7b1a11'
);

SELECT * FROM place WHERE id = '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222';

-- Update place
UPDATE place
SET price = 300.00
WHERE id = '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222';

SELECT * FROM place WHERE id = '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222';

-- Insert review
INSERT INTO review (id, text, rating, user_id, place_id)
VALUES (
    '72e1d4a0-8b0f-4f25-a8e4-61c5d8f3c333',
    'Very good place',
    5,
    '8d2f8b7d-3c96-4d72-a8df-9d1e4c7b1a11',
    '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222'
);

SELECT * FROM review WHERE id = '72e1d4a0-8b0f-4f25-a8e4-61c5d8f3c333';

-- Update review
UPDATE review
SET text = 'Excellent place'
WHERE id = '72e1d4a0-8b0f-4f25-a8e4-61c5d8f3c333';

SELECT * FROM review WHERE id = '72e1d4a0-8b0f-4f25-a8e4-61c5d8f3c333';

-- Link amenity to place
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222',
    '42308b94-293e-463a-8290-e3456d636228'
);

SELECT * FROM place_amenity
WHERE place_id = '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222';

-- Delete test records
DELETE FROM review WHERE id = '72e1d4a0-8b0f-4f25-a8e4-61c5d8f3c333';
DELETE FROM place_amenity
WHERE place_id = '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222'
  AND amenity_id = '42308b94-293e-463a-8290-e3456d636228';
DELETE FROM place WHERE id = '9a4c7f32-5e11-4d5b-9ad2-2f13e7c2b222';
DELETE FROM user WHERE id = '8d2f8b7d-3c96-4d72-a8df-9d1e4c7b1a11';
