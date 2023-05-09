from .default_test_case import DefaultTestCase
from users.models import User
from rest_framework import status
import ipdb


class CommentTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("Comment tests")
        print("=" * 50)

    def test_comment_post_success(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.post(
            self.url_posts_retrieve_comment, self.comment_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("content", response.data)
        self.assertIn("user", response.data)
        self.assertIn("post_id", response.data)

        print("test_comment_post_success - OK")

    def test_comment_post_error_invalid_json(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.post(self.url_posts_retrieve_comment, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)
        self.assertTrue("This field is required." in response.data["content"])

        print("test_comment_post_error_invalid_json - OK")

    def test_comment_post_error_not_found(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.post(
            self.url_posts_retrieve_not_found_comment, self.comment_data, format="json"
        )

        self.responseAssertNotFound(response)

        print("test_comment_post_error_not_found - OK")

    def test_comment_post_error_missing_token(self):
        self.client = self.login_apiclient(self.user_friend_login, auth=False)

        response = self.client.post(
            self.url_posts_retrieve_comment, self.comment_data, format="json"
        )

        self.responseAssertMissingToken(response)

        print("test_comment_post_error_missing_token - OK")

    def test_retrieve_comment_success(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.get(self.url_posts_retrieve_comment_retrieve)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("content", response.data)
        self.assertIn("user", response.data)
        self.assertIn("post_id", response.data)

        print("test_retrieve_comment_success - OK")

    def test_retrieve_comment_error_not_found_post(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.get(self.url_posts_retrieve_not_found_comment_retrieve)

        self.responseAssertNotFound(response)

        print("test_retrieve_comment_error_not_found_post - OK")

    def test_retrieve_comment_error_not_found_comment(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.get(self.url_posts_retrieve_comment_not_found)

        self.responseAssertNotFound(response)

        print("test_retrieve_comment_error_not_found_comment - OK")

    def test_retrieve_comment_error_missing_token(self):
        self.client = self.login_apiclient(self.user_friend_login, auth=False)

        response = self.client.get(self.url_posts_retrieve_comment)

        self.responseAssertMissingToken(response)

        print("test_retrieve_comment_error_missing_token - OK")

    def test_edit_comment_success(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.patch(
            self.url_posts_retrieve_comment_retrieve,
            self.comment_data_edit,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("content", response.data)
        self.assertIn("user", response.data)
        self.assertIn("post_id", response.data)

        self.assertEqual(self.comment_data_edit["content"], response.data["content"])

        print("test_retrieve_comment_success - OK")

    def test_edit_comment_error_not_found_post(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.patch(
            self.url_posts_retrieve_not_found_comment_retrieve,
            self.comment_data_edit,
            format="json",
        )

        self.responseAssertNotFound(response)

        print("test_edit_comment_error_not_found_post - OK")

    def test_edit_comment_error_not_found_comment(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.patch(
            self.url_posts_retrieve_comment_not_found,
            self.comment_data_edit,
            format="json",
        )

        self.responseAssertNotFound(response)

        print("test_edit_comment_error_not_found_post - OK")

    def test_edit_comment_error_missing_token(self):
        self.client = self.login_apiclient(self.user_friend_login, auth=False)

        response = self.client.patch(
            self.url_posts_retrieve_comment_retrieve,
            self.comment_data_edit,
            format="json",
        )

        self.responseAssertMissingToken(response)

        print("test_edit_comment_error_missing_token - OK")

    def test_remove_comment_success(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.delete(self.url_posts_retrieve_comment_retrieve)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        print("test_remove_comment_success - OK")

    def test_remove_comment_error_not_found_post(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.delete(
            self.url_posts_retrieve_not_found_comment_retrieve
        )

        self.responseAssertNotFound(response)

        print("test_remove_comment_error_not_found_post - OK")

    def test_remove_comment_error_not_found_comment(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.delete(self.url_posts_retrieve_comment_not_found)

        self.responseAssertNotFound(response)

        print("test_remove_comment_error_not_found_comment - OK")

    def test_remove_comment_error_missing_token(self):
        self.client = self.login_apiclient(self.user_friend_login, auth=False)

        response = self.client.delete(self.url_posts_retrieve_comment_retrieve)

        self.responseAssertMissingToken(response)

        print("test_remove_comment_error_missing_token - OK")
