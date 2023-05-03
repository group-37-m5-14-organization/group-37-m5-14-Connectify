from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "user_id", "post_id"]
        read_only_fields = ["user_id", "post_id"]

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
