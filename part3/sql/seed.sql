USE hbnb_db;

INSERT INTO user (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$anouBdkyvtFYvqSGwotKieQhSyjExdIyKUPQngFxx2G7b7iWy9tau',
    TRUE
);

INSERT INTO amenity (id, name) VALUES
('42308b94-293e-463a-8290-e3456d636228', 'WiFi'),
('1995e61a-0e8e-4389-8005-f92dd0a79a1b', 'Swimming Pool'),
('f344e5f1-c716-479a-8d0e-3939312ab6a2', 'Air Conditioning');
