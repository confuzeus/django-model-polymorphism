from django.db import models
from django.conf import settings
from polymorphic.models import PolymorphicModel


class Post(PolymorphicModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="socialpolymorphic_posts",
    )
    title = models.CharField(max_length=155)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.title}"


class TextPost(Post):
    body = models.TextField(max_length=10000)


class YoutubeEmbedPost(Post):
    video_id = models.CharField(max_length=24)


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class ImagePost(Post):
    image = models.ImageField(upload_to=user_directory_path)


class URLPost(Post):
    url = models.URLField()
