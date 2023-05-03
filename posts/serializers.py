from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        frields = ["id", "title", "img", "content", "user_id"]
        read_only_fields = ["user_id"]

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
