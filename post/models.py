import os
import uuid

from django.db import models

from config import settings


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{uuid.uuid4()}{extension}"
    return os.path.join(f"uploads/posts-image/", filename)


class Hashtag(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to=post_image_file_path,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name="posts")

    def __str__(self):
        return self.content
