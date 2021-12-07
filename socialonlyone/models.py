from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Post(models.Model):
    TEXT_POST_TYPE = 0
    YOUTUBE_POST_TYPE = 1
    IMAGE_POST_TYPE = 2
    URL_POST_TYPE = 3

    POST_TYPE_CHOICES = (
        (TEXT_POST_TYPE, "Text"),
        (YOUTUBE_POST_TYPE, "Youtube"),
        (IMAGE_POST_TYPE, "Image"),
        (URL_POST_TYPE, "URL"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="socialonlyone_posts",
    )
    title = models.CharField(max_length=155)
    post_type = models.PositiveSmallIntegerField(choices=POST_TYPE_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    text_body = models.TextField(max_length=10000, null=True, blank=True)
    youtube_video_id = models.CharField(max_length=22, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if self.post_type == self.TEXT_POST_TYPE:
            if self.text_body is None:
                raise ValidationError("Body can't be empty")

            if self.youtube_video_id or self.image or self.url:
                raise ValidationError("Text posts can only have body.")

        elif self.post_type == self.YOUTUBE_POST_TYPE:
            if self.youtube_video_id is None:
                raise ValidationError("You need to provide a video ID.")

            if self.text_body or self.image or self.url:
                raise ValidationError("Youtube posts can only have video id.")

        elif self.post_type == self.IMAGE_POST_TYPE:
            if self.image is None:
                raise ValidationError("Image required.")

            if self.text_body or self.youtube_video_id or self.url:
                raise ValidationError("Image posts can only have image")
        elif self.post_type == self.URL_POST_TYPE:
            if self.url is None:
                raise ValidationError("Url required.")
            if self.text_body or self.youtube_video_id or self.image:
                raise ValidationError("Url posts can only have url")
        return super(Post, self).clean()


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        post_type = kwargs.pop("post_type")
        super(PostForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        self.instance.post_type = post_type
        if post_type == Post.TEXT_POST_TYPE:
            self.fields["text_body"].required = True
            del self.fields["youtube_video_id"]
            del self.fields["image"]
            del self.fields["url"]
        elif post_type == Post.IMAGE_POST_TYPE:
            self.fields["image"].required = True
            del self.fields["youtube_video_id"]
            del self.fields["text_body"]
            del self.fields["url"]
        elif Post.YOUTUBE_POST_TYPE:
            self.fields["youtube_video_id"].required = True
            del self.fields["text_body"]
            del self.fields["image"]
            del self.fields["url"]
        elif Post.URL_POST_TYPE:
            self.fields["url"].required = True
            del self.fields["youtube_video_id"]
            del self.fields["image"]
            del self.fields["text_body"]
        else:
            raise ValueError("Unknown post type")

    class Meta:
        model = Post
        fields = ["title", "text_body", "youtube_video_id", "image", "url"]
