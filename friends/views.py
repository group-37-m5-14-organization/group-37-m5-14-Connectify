from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Friend
from .serializers import FriendSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import pagination
import ipdb


class CreateDestroyListFriendRequestView(
    generics.ListCreateAPIView,
    generics.DestroyAPIView,
    generics.UpdateAPIView,
):
    authentication_classes = [JWTAuthentication]
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    lookup_url_kwarg = "pk"

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        received = Friend.objects.filter(receive_user=user, status=True)
        sent = Friend.objects.filter(send_user=user, status=True)
        queryset = received | sent

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receive_user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        if self.request.user == receive_user:
            return Response(
                {"message": "Cannot add yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verify_user_logged = Friend.objects.filter(
            send_user=self.request.user, receive_user=receive_user
        )
        verify_user_wanted = Friend.objects.filter(
            send_user=receive_user, receive_user=self.request.user
        )
        if verify_user_wanted or verify_user_logged:
            return Response(
                {"message": "Request or friend already exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer, receive_user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, receive_user):
        return serializer.save(send_user=self.request.user, receive_user=receive_user)
    
    def perform_update(self, serializer):
        return serializer.save(status=True)

    def destroy(self, request, *args, **kwargs):
        find_user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        verify_friend_exist = Friend.objects.filter(
            send_user=self.request.user, receive_user=find_user
        )
        verify_friend_exist_inverted = Friend.objects.filter(
            send_user=find_user, receive_user=self.request.user
        )
        if len(verify_friend_exist) < 1 and len(verify_friend_exist_inverted) < 1:
            return Response(
                {"message": "Friendship or request not find."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.perform_destroy(
            verify_friend_exist
            if len(verify_friend_exist) > 0
            else verify_friend_exist_inverted
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        send_user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        verify = get_object_or_404(
            Friend, send_user=send_user, receive_user=self.request.user
        )
        return verify


class ListFriendRequestView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = FriendSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return Friend.objects.filter(receive_user=self.request.user, status=False)
