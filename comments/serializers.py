from rest_framework import serializers
from .models import Comment

from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "user", "post_id"]
        read_only_fields = ["user", "post_id"]

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
