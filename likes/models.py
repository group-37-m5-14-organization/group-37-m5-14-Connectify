from django.db import models


class Like(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="likes"
    )
