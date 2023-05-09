from django.db import models


class Friend(models.Model):
    send_user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="requesting_users"
    )
    receive_user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="request_users"
    )
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
