import unittest

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestNotesAPI(unittest.TestCase):
    def test_hello_world(self):
        response = client.get("/")
        self.assertEqual(response.json(), {"message": "Hello World"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
