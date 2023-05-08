from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import View

from friends.models import Friend
from follows.models import Follow

from users.models import User


class FriendsPostOrOnlyPublics(BasePermission):
    def has_object_permission(self, request, _: View, obj: User) -> bool:

        if request.method in SAFE_METHODS:
            if not obj.is_private:

                return True
            
            else:
                return (Friend.objects.filter(
                        send_user=obj.user.id, receive_user=request.user.id, status=True).exists()

                    or Friend.objects.filter(
                        send_user=request.user.id, receive_user=obj.user.id, status=True).exists()

                    or Follow.objects.filter(followed_user=obj.user.id).exists()
                    or obj.user == request.user)
        
        return (request.user.is_authenticated and request.user == obj.user)