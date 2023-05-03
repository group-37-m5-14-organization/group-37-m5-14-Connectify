from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=127)
    content = models.TextField()
    img = models.CharField(max_length=255)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )
