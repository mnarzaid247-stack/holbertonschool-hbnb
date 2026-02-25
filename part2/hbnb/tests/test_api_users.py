import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_create_user_success(self):
        res = self.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertIn(res.status_code, (200, 201))
        data = res.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["email"], "john.doe@example.com")

    def test_create_user_invalid(self):
        res = self.client.post("/api/v1/users/", json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(res.status_code, 400)

    def test_get_user_not_found(self):
        res = self.client.get("/api/v1/users/does-not-exist")
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
