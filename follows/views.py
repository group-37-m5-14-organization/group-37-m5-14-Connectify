from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Follow
from .serializers import FollowSerializer
from users.models import User
from django.shortcuts import get_object_or_404


class FollowView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        print(self.__dict__)
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        serializer.save(followed_user=user)

class FollowDestroyView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_url_kwarg = "pk"

class FollowedListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = FollowSerializer

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get("pk"))
        return Follow.objects.filter(user=user)
    
class FollowListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = FollowSerializer

    def get_queryset(self):
        followed_user = User.objects.get(pk=self.kwargs.get("pk"))
        return Follow.objects.filter(followed_user=followed_user)
