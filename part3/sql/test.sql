USE hbnb_db;

-- Check seed data
SELECT * FROM user;
SELECT * FROM amenity;

-- Insert test user
INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'John',
    'Doe',
    'john@example.com',
    '$2b$12$abcdefghijklmnopqrstuvabcdefghijklmnopqrstuvabcd',
    FALSE
);

-- Read user
SELECT * FROM user WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

-- Update user
UPDATE user
SET first_name = 'Johnny'
WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

SELECT * FROM user WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

-- Insert place
INSERT INTO place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    'Nice Apartment',
    'City center',
    250.00,
    24.7136,
    46.6753,
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
);

SELECT * FROM place;

-- Update place
UPDATE place
SET price = 300.00
WHERE id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';

SELECT * FROM place WHERE id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';

-- Insert review
INSERT INTO review (id, text, rating, user_id, place_id)
VALUES (
    'cccccccc-cccc-cccc-cccc-cccccccccccc',
    'Very good place',
    5,
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
);

SELECT * FROM review;

-- Update review
UPDATE review
SET text = 'Excellent place'
WHERE id = 'cccccccc-cccc-cccc-cccc-cccccccccccc';

SELECT * FROM review WHERE id = 'cccccccc-cccc-cccc-cccc-cccccccccccc';

-- Link amenity to place
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    '11111111-1111-1111-1111-111111111111'
);

SELECT * FROM place_amenity;

-- Delete test records
DELETE FROM review WHERE id = 'cccccccc-cccc-cccc-cccc-cccccccccccc';
DELETE FROM place_amenity
WHERE place_id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
  AND amenity_id = '11111111-1111-1111-1111-111111111111';
DELETE FROM place WHERE id = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';
DELETE FROM user WHERE id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
