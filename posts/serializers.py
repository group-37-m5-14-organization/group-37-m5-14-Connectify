from rest_framework.serializers import ModelSerializer
from .models import Post


class PostSerializer(ModelSerializer):
    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    class Meta:
        model = Post
        fields = ["id", "title", "img", "content", "user_id"]
        read_only_fields = ["user_id"]

