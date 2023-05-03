from django.db import models


class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="comments"
    )
