from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList
from posts.models import Post
from comments.models import Comment
import ipdb


class DefaultTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ...

    @classmethod
    def setUpClass(cls):
        cls.user_request = {
            "username": "pedro",
            "email": "pedro@mail.com",
            "password": "123456",
            "first_name": "Pedro",
            "last_name": "Carvalho",
        }

        cls.user_friend_request = {
            "username": "fernando",
            "email": "fernando@mail.com",
            "password": "123456",
            "first_name": "Fernando",
            "last_name": "Oliveira",
        }

        cls.user_login = {"username": "pedro", "password": "123456"}
        cls.user_friend_login = {"username": "fernando", "password": "123456"}

        cls.post_data = {
            "title": "Primeiro post",
            "content": "Esse é o primeiro post desse usuário",
            "img": "https://s.dicio.com.br/post.jpg",
        }

        cls.post_data_edit = {"title": "Primeiro post"}

        cls.comment_data = {"content": "comentario"}

        cls.comment_data_edit = {"content": "comentario editado"}

        cls.url_login = "/api/users/login/"

        cls.url_posts = "/api/posts/"

        cls.message_test()

    @classmethod
    def tearDownClass(cls):
        print("=" * 50)

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create_user(**cls.user_request)
        cls.user_friend = User.objects.create_user(**cls.user_friend_request)

        cls.post_public = Post.objects.create(**cls.post_data, user=cls.user)
        cls.comment = Comment.objects.create(
            **cls.comment_data, user=cls.user_friend, post=cls.post_public
        )

        cls.url_posts_retrieve = f"{cls.url_posts}{cls.post_public.id}/"
        cls.url_posts_retrieve_not_found = f"{cls.url_posts}99999/"
        cls.url_posts_retrieve_like = f"{cls.url_posts}{cls.post_public.id}/like/"
        cls.url_posts_retrieve_not_found_like = f"{cls.url_posts}99999/like/"
        cls.url_posts_retrieve_comment = f"{cls.url_posts}{cls.post_public.id}/comment/"
        cls.url_posts_retrieve_not_found_comment = f"{cls.url_posts}99999/comment/"
        cls.url_posts_retrieve_comment_retrieve = (
            f"{cls.url_posts}{cls.post_public.id}/comment/{cls.comment.id}/"
        )
        cls.url_posts_retrieve_not_found_comment_retrieve = (
            f"{cls.url_posts}99999/comment/{cls.comment.id}/"
        )
        cls.url_posts_retrieve_comment_not_found = (
            f"{cls.url_posts}{cls.post_public.id}/comment/99999/"
        )

    @classmethod
    def message_test(cls):
        print("=" * 50)

    @classmethod
    def login_apiclient(cls, login_data, auth=True):
        client_login = APIClient()

        if not auth:
            return client_login

        login_response = client_login.post(cls.url_login, login_data, format="json")
        token = login_response.data["access"]

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        return client

    def responseAssertMissingToken(self, response):
        """Response detail: Authentication credentials were not provided."""
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual(
            str(response.data["detail"]),
            "Authentication credentials were not provided.",
        )

    def responseAssertNotAuthorized(self, response):
        """Response detail: You do not have permission to perform this action."""
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual(
            str(response.data["detail"]),
            "You do not have permission to perform this action.",
        )

    def responseAssertNotFound(self, response):
        """Response detail: not found."""
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("Not found.", str(response.data["detail"]))

    def responseAssertPaginatedList(self, response):
        """Response paginated list"""
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertIsInstance(response.data["results"], ReturnList)
