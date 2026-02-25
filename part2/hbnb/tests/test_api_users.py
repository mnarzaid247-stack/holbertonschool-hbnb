import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_01_create_user_success(self):
        res = self.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["email"], "john.doe@example.com")

    def test_02_create_user_invalid_data(self):
        res = self.client.post("/api/v1/users/", json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(res.status_code, 400)

    def test_03_create_user_duplicate_email(self):
        # create first
        self.client.post("/api/v1/users/", json={
            "first_name": "A",
            "last_name": "B",
            "email": "dup@example.com"
        })
        # create duplicate
        res = self.client.post("/api/v1/users/", json={
            "first_name": "C",
            "last_name": "D",
            "email": "dup@example.com"
        })
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("error", data)

    def test_04_get_user_not_found(self):
        res = self.client.get("/api/v1/users/does-not-exist")
        self.assertEqual(res.status_code, 404)

    def test_05_get_user_success(self):
        created = self.client.post("/api/v1/users/", json={
            "first_name": "Sara",
            "last_name": "Ali",
            "email": "sara.ali@example.com"
        })
        user_id = created.get_json()["id"]

        res = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["id"], user_id)

    def test_06_update_user_not_found(self):
        res = self.client.put("/api/v1/users/does-not-exist", json={
            "first_name": "X",
            "last_name": "Y",
            "email": "x@y.com"
        })
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
