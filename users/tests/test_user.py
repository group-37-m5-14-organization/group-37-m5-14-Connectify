from .default_test_case import DefaultTestCase
from ..models import User
from rest_framework import status
import ipdb


class UserTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("User tests")
        print("=" * 50)

    def test_retrieve_user_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_retrieve_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

        self.assertIsInstance(response.data["id"], int)
        self.assertIsInstance(response.data["username"], str)
        self.assertIsInstance(response.data["email"], str)
        self.assertIsInstance(response.data["first_name"], str)
        self.assertIsInstance(response.data["last_name"], str)

        print("test_retrieve_user_success - OK")

    def test_retrieve_user_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_retrieve_user_not_found)

        self.responseAssertNotFound(response)

        print("test_follow_user_error_not_found - OK")

    def test_list_user_posts_without_auth_success(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_user_posts)

        self.responseAssertPaginatedList(response)

        print("test_list_user_posts_without_auth_success - OK")

    def test_list_user_posts_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_user_posts)

        self.responseAssertPaginatedList(response)

        print("test_retrieve_user_success - OK")

    def test_list_user_posts_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_user_not_found_posts)

        self.responseAssertNotFound(response)

        print("test_retrieve_user_success - OK")
