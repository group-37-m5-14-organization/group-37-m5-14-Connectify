from .default_test_case import DefaultTestCase
from ..models import User
from rest_framework import status
import ipdb


class FollowTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("Follow tests")
        print("=" * 50)

    def test_follow_user_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.post(self.url_follow)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("user", response.data)
        self.assertIn("followed_user", response.data)

        self.assertIsInstance(response.data["id"], int)
        self.assertIsInstance(response.data["user"], int)
        self.assertIsInstance(response.data["followed_user"], int)

        print("test_follow_user_success - OK")

    def test_follow_user_error_already_following(self):
        self.client = self.login_apiclient(self.user_login)

        self.client.post(self.url_follow)

        response = self.client.post(self.url_follow)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Already follow this user.")

        print("test_follow_user_error_already_following - OK")

    def test_follow_user_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.post(self.url_user_not_found)

        self.responseAssertNotFound(response)

        print("test_follow_user_error_not_found - OK")

    def test_list_followers_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_followers)

        self.responseAssertPaginatedList(response)

        print("test_list_followers_success - OK")

    def test_list_followers_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_followers)

        self.responseAssertMissingToken(response)

        print("test_list_followers_error_missing_token - OK")

    def test_list_following_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_followers)

        self.responseAssertPaginatedList(response)

        print("test_list_following_success - OK")

    def test_list_following_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_followers)

        self.responseAssertMissingToken(response)

        print("test_list_following_error_missing_token - OK")
