from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


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
        related_name="socialjson_posts",
    )
    title = models.CharField(max_length=155)
    post_type = models.PositiveSmallIntegerField(choices=POST_TYPE_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    data = models.JSONField()

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.title}"

    def clean(self):

        if self.post_type == self.TEXT_POST_TYPE:
            try:
                self.data["text_body"]
            except KeyError:
                raise ValidationError('Text posts must contain "text_body"')
        elif self.post_type == self.IMAGE_POST_TYPE:
            try:
                self.data["image"]
            except KeyError:
                raise ValidationError('Image posts must contain "image"')
        elif self.post_type == self.YOUTUBE_POST_TYPE:
            try:
                self.data["video_id"]
            except KeyError:
                raise ValidationError('Youtube posts must contain "video_id"')
        elif self.post_type == self.URL_POST_TYPE:
            try:
                self.data["url"]
            except KeyError:
                raise ValidationError('Url posts must contain "url"')
        return super(Post, self).clean()


class PostForm(forms.Form):
    title = forms.CharField(max_length=155)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        post_type = kwargs.pop("post_type")
        self.post_type = post_type

        super(PostForm, self).__init__(*args, **kwargs)

        if post_type == Post.TEXT_POST_TYPE:
            self.fields["body"] = forms.CharField(max_length=10000)
        elif post_type == Post.IMAGE_POST_TYPE:
            self.fields["image"] = forms.ImageField()
        elif post_type == Post.YOUTUBE_POST_TYPE:
            self.fields["video_id"] = forms.CharField(max_length=25)
        elif post_type == Post.URL_POST_TYPE:
            self.fields["url"] = forms.URLField()
        else:
            raise ValueError("Unknown post type.")

    def save(self):
        data = {}
        if self.post_type == Post.TEXT_POST_TYPE:
            data["text_body"] = self.cleaned_data["body"]
        elif self.post_type == Post.IMAGE_POST_TYPE:
            image_field = self.cleaned_data["image"]
            filename = image_field.name.replace(" ", "_")
            destination_path = settings.MEDIA_ROOT / self.user.username
            destination_path.mkdir(parents=True, exist_ok=True)
            with (destination_path / filename).open("wb+") as destination:
                for chunk in image_field.chunks():
                    destination.write(chunk)
            data["image"] = f"{settings.MEDIA_URL}{self.user.username}/{filename}"
        elif self.post_type == Post.YOUTUBE_POST_TYPE:
            data["video_id"] = self.cleaned_data["video_id"]
        else:
            data["url"] = self.cleaned_data["url"]

        post = Post(
            user=self.user,
            post_type=self.post_type,
            title=self.cleaned_data["title"],
            data=data,
        )
        post.full_clean()
        post.save()
