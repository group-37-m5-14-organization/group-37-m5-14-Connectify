from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "user", "followed_user"]
        read_only_fields = ["user", "followed_user"]

    def create(self, validated_data):
        return Follow.objects.create(**validated_data)
