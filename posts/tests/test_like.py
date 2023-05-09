from .default_test_case import DefaultTestCase
from users.models import User
from rest_framework import status
import ipdb


class LikeTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("Like tests")
        print("=" * 50)

    def test_like_post_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.post(self.url_posts_retrieve_like)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("detail", response.data)

        self.assertIsInstance(response.data["detail"], str)
        self.assertEqual(response.data["detail"], "Post curtido com sucesso!")

        print("test_retrieve_user_success - OK")

    def test_like_post_error_already_liked(self):
        self.client = self.login_apiclient(self.user_login)

        self.client.post(self.url_posts_retrieve_like)

        response = self.client.post(self.url_posts_retrieve_like)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("detail", response.data)

        self.assertIsInstance(response.data["detail"], str)
        self.assertEqual(response.data["detail"], "Você já curtiu esse post.")

        print("test_like_post_error_already_liked - OK")

    def test_like_post_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.post(self.url_posts_retrieve_like)

        self.responseAssertMissingToken(response)

        print("test_like_post_error_missing_token - OK")

    def test_like_post_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.post(self.url_posts_retrieve_not_found_like)

        self.responseAssertNotFound(response)

        print("test_like_post_error_not_found - OK")

    def test_unlike_post_success(self):
        self.client = self.login_apiclient(self.user_login)

        self.client.post(self.url_posts_retrieve_like)

        response = self.client.delete(self.url_posts_retrieve_like)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        print("test_unlike_post_success - OK")

    def test_unlike_post_error_not_liked(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.delete(self.url_posts_retrieve_like)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("detail", response.data)

        self.assertIsInstance(response.data["detail"], str)
        self.assertEqual(response.data["detail"], "Você ainda não curtiu esse post.")

        print("test_unlike_post_error_not_liked - OK")

    def test_unlike_post_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.delete(self.url_posts_retrieve_like)

        self.responseAssertMissingToken(response)

        print("test_unlike_post_error_missing_token - OK")

    def test_unlike_post_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.delete(self.url_posts_retrieve_not_found_like)

        self.responseAssertNotFound(response)

        print("test_unlike_post_error_not_found - OK")
