import unittest

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class TestModels(unittest.TestCase):

    def test_user_creation(self):
        u = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.assertIsInstance(u.id, str)
        self.assertTrue(len(u.id) > 0)
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")
        self.assertEqual(u.email, "john.doe@example.com")

    def test_amenity_creation(self):
        a = Amenity(name="Wi-Fi")
        self.assertIsInstance(a.id, str)
        self.assertEqual(a.name, "Wi-Fi")

    def test_place_creation_and_validation(self):
        owner = User(first_name="A", last_name="B", email="a@b.com")
        p = Place(title="Nice place", price=100, owner_id=owner.id)
        self.assertEqual(p.title, "Nice place")
        self.assertEqual(p.owner_id, owner.id)
        self.assertTrue(p.price > 0)

        # invalid title
        with self.assertRaises(ValueError):
            Place(title="   ", price=100, owner_id=owner.id)

        # invalid price
        with self.assertRaises(ValueError):
            Place(title="X", price=0, owner_id=owner.id)

    def test_place_relationship_methods(self):
        owner = User(first_name="A", last_name="B", email="a@b.com")
        p = Place(title="T", price=50, owner_id=owner.id)

        # Make sure lists exist
        self.assertTrue(hasattr(p, "amenity_ids"))
        self.assertTrue(hasattr(p, "review_ids"))

        a = Amenity(name="Parking")
        p.add_amenity(a)
        self.assertIn(a.id, p.amenity_ids)

        r = Review(text="Great", rating=5, user_id=owner.id, place_id=p.id)
        p.add_review(r)
        self.assertIn(r.id, p.review_ids)


if __name__ == "__main__":
    unittest.main()
