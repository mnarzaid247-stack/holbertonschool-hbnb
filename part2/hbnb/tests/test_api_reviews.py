import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def _create_user(self, email="review.user@example.com"):
        res = self.client.post("/api/v1/users/", json={
            "first_name": "Review",
            "last_name": "User",
            "email": email
        })
        self.assertIn(res.status_code, (200, 201))
        return res.get_json()["id"]

    def _create_place(self, owner_id):
        # Adjust keys if your places endpoint requires more fields
        res = self.client.post("/api/v1/places/", json={
            "title": "Test Place",
            "price": 100,
            "owner_id": owner_id
        })
        self.assertIn(res.status_code, (200, 201))
        return res.get_json()["id"]

    def test_01_create_review_success(self):
        user_id = self._create_user(email="review.success@example.com")
        place_id = self._create_place(owner_id=user_id)

        res = self.client.post("/api/v1/reviews/", json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertIn(res.status_code, (200, 201))
        data = res.get_json()
        self.assertIn("id", data)
        self.assertEqual(data.get("text"), "Great place!")
        self.assertEqual(data.get("rating"), 5)

    def test_02_create_review_invalid_text(self):
        user_id = self._create_user(email="review.invalid@example.com")
        place_id = self._create_place(owner_id=user_id)

        res = self.client.post("/api/v1/reviews/", json={
            "text": "",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(res.status_code, 400)

    def test_03_get_review_not_found(self):
        res = self.client.get("/api/v1/reviews/does-not-exist")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
