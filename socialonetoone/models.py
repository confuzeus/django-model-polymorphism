from django import forms
from django.db import models
from django.conf import settings


class TextPost(models.Model):
    body = models.TextField(max_length=10000)


class YoutubeEmbedPost(models.Model):
    video_id = models.CharField(max_length=24)


class ImagePost(models.Model):
    image = models.ImageField()


class URLPost(models.Model):
    url = models.URLField()


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="socialonetoone_posts",
    )
    title = models.CharField(max_length=155)
    date_added = models.DateTimeField(auto_now_add=True)

    text_post = models.OneToOneField(TextPost, on_delete=models.CASCADE, null=True)
    youtube_post = models.OneToOneField(
        YoutubeEmbedPost, on_delete=models.CASCADE, null=True
    )
    image_post = models.OneToOneField(ImagePost, on_delete=models.CASCADE, null=True)
    url_post = models.OneToOneField(URLPost, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.title}"


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        post_type = kwargs.pop("post_type")
        super(PostForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        self.post_type = post_type

        if post_type == "text":
            self.fields["body"] = forms.CharField(
                widget=forms.Textarea(), max_length=10_000
            )
        elif post_type == "image":
            self.fields["image"] = forms.ImageField()
        elif post_type == "youtube":
            self.fields["video_id"] = forms.CharField(max_length=25)
        elif post_type == "url":
            self.fields["url"] = forms.URLField
        else:
            raise ValueError("Unknown post type.")

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        if self.post_type == "text":
            text_post = TextPost(body=cleaned_data["body"])
            text_post.full_clean()
            text_post.save()
            self.instance.text_post = text_post
        elif self.post_type == "image":
            image_post = ImagePost(image=cleaned_data["image"])
            image_post.full_clean()
            image_post.save()
            self.instance.image_post = image_post
        elif self.post_type == "youtube":
            youtube_post = YoutubeEmbedPost(video_id=cleaned_data["video_id"])
            youtube_post.full_clean()
            youtube_post.save()
            self.instance.youtube_post = youtube_post
        else:
            url_post = URLPost(url=cleaned_data["url"])
            url_post.full_clean()
            url_post.save()
            self.instance.url_post = url_post
        return cleaned_data

    class Meta:
        model = Post
        fields = ["title"]
