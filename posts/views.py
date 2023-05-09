from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import FriendsPostOrOnlyPublics
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer
from friends.models import Friend

from follows.models import Follow
from .models import Post
from users.models import User


class PostDetailsView(RetrieveUpdateDestroyAPIView):  # Post retrieve, update n delete
    authentication_classes = [JWTAuthentication]
    permission_classes = [FriendsPostOrOnlyPublics]

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SelfPostsView(ListAPIView):  # List self posts
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostView(ListCreateAPIView, PageNumberPagination):  # Timeline
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        send_frendship = Friend.objects.filter(
            send_user=self.request.user.id, status=True
        )

        receive_frindship = Friend.objects.filter(
            receive_user=self.request.user.id, status=True
        )

        following = Follow.objects.filter(user_id=self.request.user.id)
        friends = send_frendship | receive_frindship

        ids = []

        for follow in following:
            ids.append(follow.followed_user.id)

        for i in friends:
            ids.append(i.receive_user.id), ids.append(i.send_user.id)

        restrict_posts = Post.objects.filter(user_id__in=ids)

        return restrict_posts

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPostsView(ListAPIView):  # List posts by user_id
    authentication_classes = [JWTAuthentication]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        posts_owner = get_object_or_404(User, id=self.kwargs.get("pk"))
        query = Post.objects.filter(user_id=posts_owner.id)

        if not self.request.user.is_authenticated:
            return query.filter(is_private=False)

        if (
            Friend.objects.filter(
                send_user=posts_owner.id, receive_user=self.request.user.id, status=True
            ).exists()
            or Friend.objects.filter(
                send_user=self.request.user.id, receive_user=posts_owner.id, status=True
            ).exists()
            or Follow.objects.filter(followed_user=posts_owner.id).exists()
            or posts_owner == self.request.user
        ):
            return query

        else:
            return query.filter(is_private=False)
