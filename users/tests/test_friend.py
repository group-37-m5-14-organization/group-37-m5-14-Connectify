# from django.test import TestCase
from .default_test_case import DefaultTestCase

# from rest_framework.test import APIClient
from ..models import User
from rest_framework import status
import ipdb

from rest_framework.utils.serializer_helpers import ReturnList


class FriendTest(DefaultTestCase):
    @classmethod
    def message_test(cls):
        print("=" * 50)
        print("Friend tests")
        print("=" * 50)

    def test_request_friend_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.post(self.url_friend)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("send_user", response.data)
        self.assertIn("receive_user", response.data)
        self.assertIn("status", response.data)
        self.assertTrue(not response.data["status"])

        print("test_success_request_friend - OK")

    def test_request_friend_error_cannot_add_yourself(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.post(self.url_user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Cannot add yourself.")

        print("test_request_friend_error_cannot_add_yourself - OK")

    def test_request_friend_error_cannot_request_if_already_exist(self):
        self.client = self.login_apiclient(self.user_login)

        self.client.post(self.url_friend)

        response = self.client.post(self.url_friend)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Request or friend already exist.")

        print("test_request_friend_error_cannot_request_if_already_exist - OK")

    def test_request_friend_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.post(self.url_friend)

        self.responseAssertMissingToken(response)

        print("test_request_friend_error_missing_token - OK")

    def test_accept_friend_success(self):
        self.client = self.login_apiclient(self.user_login)
        self.client.post(self.url_friend)

        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.patch(self.url_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("send_user", response.data)
        self.assertIn("receive_user", response.data)
        self.assertIn("status", response.data)
        self.assertTrue(response.data["status"])

        print("test_accept_friend_success - OK")

    def test_accept_friend_error_not_found_request(self):
        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.patch(self.url_user)

        self.responseAssertNotFound(response)

        print("test_accept_friend_error_not_found_request - OK")

    def test_accept_friend_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.patch(self.url_friend)

        self.responseAssertMissingToken(response)

        print("test_accept_friend_error_missing_token - OK")

    def test_unfriend_or_unaccept_success(self):
        self.client = self.login_apiclient(self.user_login)
        self.client.post(self.url_friend)

        response = self.client.delete(self.url_friend)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.post(self.url_friend)

        self.client = self.login_apiclient(self.user_friend_login)

        response = self.client.delete(self.url_user)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        print("test_unfriend_or_unaccept_success - OK")

    def test_unfriend_or_unaccept_error_not_found(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.patch(self.url_friend)

        self.responseAssertNotFound(response)

        print("test_unfriend_or_unaccept_error_not_found - OK")

    def test_unfriend_or_unaccept_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.delete(self.url_friend)

        self.responseAssertMissingToken(response)

        print("test_unfriend_or_unaccept_error_missing_token - OK")

    def test_list_friend_requests_success(self):
        self.client = self.login_apiclient(self.user_login)

        response = self.client.get(self.url_requests)

        self.responseAssertPaginatedList(response)

        print("test_list_friend_requests_success - OK")

    def test_list_friend_requests_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_requests)

        self.responseAssertMissingToken(response)

        print("test_list_friend_requests_error_missing_token - OK")

    def test_list_friends_success(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_friend)

        self.responseAssertPaginatedList(response)

        print("test_list_friends_success - OK")

    def test_list_friends_error_missing_token(self):
        self.client = self.login_apiclient(self.user_login, auth=False)

        response = self.client.get(self.url_requests)

        self.responseAssertMissingToken(response)

        print("test_list_friend_requests_error_missing_token - OK")
