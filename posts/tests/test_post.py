from .default_test_case import DefaultTestCase
from users.models import User
from rest_framework import status
import ipdb


class PostTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("Post tests")
        print("=" * 50)

    def test_create_post_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.post(self.url_posts, self.post_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("img", response.data)
        self.assertIn("content", response.data)
        self.assertIn("is_private", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("user", response.data)

        self.assertIsInstance(response.data["id"], int)
        self.assertIsInstance(response.data["title"], str)
        self.assertIsInstance(response.data["img"], str)
        self.assertIsInstance(response.data["content"], str)
        self.assertIsInstance(response.data["is_private"], bool)

        print("test_retrieve_user_success - OK")

    def test_create_post_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.post(self.url_posts, self.post_data, format="json")

        self.responseAssertMissingToken(response)

        print("test_create_post_error_missing_token - OK")

    def test_list_post_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_posts)

        self.responseAssertPaginatedList(response)

        print("test_list_post_success - OK")

    def test_list_post_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_posts)

        self.responseAssertMissingToken(response)

        print("test_list_post_error_missing_token - OK")

    def test_retrieve_post_public_success(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_posts_retrieve)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("img", response.data)
        self.assertIn("content", response.data)
        self.assertIn("is_private", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("user", response.data)

        self.assertIsInstance(response.data["id"], int)
        self.assertIsInstance(response.data["title"], str)
        self.assertIsInstance(response.data["img"], str)
        self.assertIsInstance(response.data["content"], str)
        self.assertIsInstance(response.data["is_private"], bool)

        print("test_retrieve_post_public_success - OK")

    def test_retrieve_post_error_not_found(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_posts_retrieve_not_found)

        self.responseAssertNotFound(response)

        print("test_retrieve_post_error_not_found - OK")

    def test_edit_post_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.patch(
            self.url_posts_retrieve, self.post_data_edit, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("img", response.data)
        self.assertIn("content", response.data)
        self.assertIn("is_private", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("user", response.data)

        self.assertIsInstance(response.data["id"], int)
        self.assertIsInstance(response.data["title"], str)
        self.assertIsInstance(response.data["img"], str)
        self.assertIsInstance(response.data["content"], str)
        self.assertIsInstance(response.data["is_private"], bool)

        self.assertEqual(response.data["title"], self.post_data_edit["title"])

        print("test_edit_post_success - OK")

    def test_edit_post_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.patch(
            self.url_posts_retrieve_not_found, self.post_data_edit, format="json"
        )

        self.responseAssertNotFound(response)

        print("test_edit_post_error_not_found - OK")

    def test_edit_post_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.patch(
            self.url_posts_retrieve, self.post_data_edit, format="json"
        )

        self.responseAssertMissingToken(response)

        print("test_edit_post_error_missing_token - OK")

    def test_edit_post_error_not_authorized(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.patch(
            self.url_posts_retrieve, self.post_data_edit, format="json"
        )

        self.responseAssertNotAuthorized(response)

        print("test_edit_post_error_not_authorized - OK")

    def test_remove_post_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.delete(self.url_posts_retrieve)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        print("test_remove_post_success - OK")

    def test_remove_post_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.delete(self.url_posts_retrieve_not_found)

        self.responseAssertNotFound(response)

        print("test_remove_post_error_not_found - OK")

    def test_remove_post_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.delete(self.url_posts_retrieve)

        self.responseAssertMissingToken(response)

        print("test_remove_post_error_missing_token - OK")

    def test_remove_post_error_not_authorized(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.delete(self.url_posts_retrieve)

        self.responseAssertNotAuthorized(response)

        print("test_remove_post_error_not_authorized - OK")
