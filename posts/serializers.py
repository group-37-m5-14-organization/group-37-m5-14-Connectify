from rest_framework.serializers import ModelSerializer
from .models import Post
from users.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance: Post, data: dict) -> Post:
        return super().update(instance, data)

    class Meta:
        model = Post
        fields = ["id", "title", "img", "content", "is_private", "created_at", "user"]
        read_only_fields = ["user", "created_at"]
        
