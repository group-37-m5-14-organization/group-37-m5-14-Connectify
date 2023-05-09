from django.db import models


class Follow(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="following_users"
    )
    followed_user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="followers_users"
    )

    class Meta:
        ordering = ["id"]
