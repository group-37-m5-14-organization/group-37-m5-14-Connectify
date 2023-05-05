from django.shortcuts import render
from rest_framework.views import APIView, status
from .models import Like
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int):
        post_id = pk
        user_id = request.user.id
        like, created = Like.objects.get_or_create(post_id=post_id, user_id=user_id)
        if not created:
            return Response({"detail": "Você já curtiu esse post."})
        return Response(
            {"detail": "Post curtido com sucesso!"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk: int):
        post_id = pk
        user_id = request.user.id
        like = Like.objects.filter(post_id=post_id, user_id=user_id).first()
        if not like:
            return Response({"detail": "Você ainda não curtiu esse post."})
        like.delete()
        return Response(
            {"detail": "Like removido com sucesso."}, status=status.HTTP_204_NO_CONTENT
        )
