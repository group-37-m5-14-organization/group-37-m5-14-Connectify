from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Follow
from .serializers import FollowSerializer
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class FollowView(generics.CreateAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "pk"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        followed_user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        if self.request.user == followed_user:
            return Response(
                {"message": "Cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verify_already_follow = Follow.objects.filter(
            user=self.request.user, followed_user=followed_user
        ).exists()

        if verify_already_follow:
            return Response(
                {"message": "Already follow this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer, followed_user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, followed_user):
        return serializer.save(user=self.request.user, followed_user=followed_user)

    def destroy(self, request, *args, **kwargs):
        find_user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        follower_exists = Follow.objects.filter(
            user=self.request.user, followed_user=find_user
        )
        follower_exists_inverted = Follow.objects.filter(
            user=find_user, followed_user=self.request.user
        )
        if len(follower_exists) < 1 and len(follower_exists_inverted) < 1:
            return Response(
                {"message": "Follower not find."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.perform_destroy(
            follower_exists if len(follower_exists) > 0 else follower_exists_inverted
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        verify = get_object_or_404(Follow, user=user, followed_user=self.request.user)
        return verify


class FollowersListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(followed_user=self.request.user)


class FollowingListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
