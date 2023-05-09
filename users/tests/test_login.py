from django.test import TestCase
from rest_framework.test import APIClient
from ..models import User
from rest_framework import status


class LoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print("=" * 50)
        print("Login tests")
        print("=" * 50)

    @classmethod
    def tearDownClass(cls):
        print("=" * 50)

    def setUp(self):
        self.client = APIClient()

        self.url = "/api/users/login/"

        self.user_request = {
            "username": "pedro",
            "email": "pedro@mail.com",
            "password": "123456",
            "first_name": "Pedro",
            "last_name": "Carvalho",
        }

        self.user_login = {"username": "pedro", "password": "123456"}
        self.user_login_invalid = {"username": "pedro", "password": "1234"}
        self.invalid_login = {"username": "pedro"}

        self.user = User.objects.create_user(**self.user_request)

    def test_success_login_user(self):
        response = self.client.post(self.url, self.user_login, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        print("test_success_login_user - OK")

    def test_invalid_login_user(self):
        response = self.client.post(self.url, self.user_login_invalid, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )

        print("test_invalid_login_user - OK")

    def test_invalid_json_login_user(self):
        response = self.client.post(self.url, self.invalid_login, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertTrue("This field is required." in response.data["password"])

        print("test_invalid_json_login_user - OK")
