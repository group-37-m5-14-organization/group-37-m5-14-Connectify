from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user_id", "post_id"]
        read_only_fields = ["user_id", "post_id"]

    def create(self, validated_data):
        return Like.objects.create(**validated_data)
