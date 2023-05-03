from rest_framework import serializers
from .models import Friend


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ["id", "send_user", "receive_user", "status"]
        read_only_fields = ["send_user", "receive_user", "status"]

    def create(self, validated_data):
        return Friend.objects.create(**validated_data)
