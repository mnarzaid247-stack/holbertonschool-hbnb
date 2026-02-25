import unittest
from app import create_app


class TestAmenityEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_01_create_amenity_success(self):
        res = self.client.post("/api/v1/amenities/", json={"name": "WiFi"})
        self.assertIn(res.status_code, (200, 201))
        data = res.get_json()
        self.assertIn("id", data)
        self.assertEqual(data.get("name"), "WiFi")

    def test_02_create_amenity_invalid(self):
        res = self.client.post("/api/v1/amenities/", json={"name": ""})
        self.assertEqual(res.status_code, 400)

    def test_03_get_amenity_not_found(self):
        res = self.client.get("/api/v1/amenities/does-not-exist")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
