from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from . import models


def post_list(request):
    ctx = {}
    posts = []
    for text_post in models.TextPost.objects.all():
        posts.append({"post": text_post, "post_type": "text"})

    for youtube_post in models.YoutubeEmbedPost.objects.all():
        posts.append({"post": youtube_post, "post_type": "youtube"})

    for image_post in models.ImagePost.objects.all():
        posts.append({"post": image_post, "post_type": "image"})

    for url_post in models.URLPost.objects.all():
        posts.append({"post": url_post, "post_type": "url"})

    page = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)
    page_obj = paginator.page(page)
    ctx.update({"page_obj": page_obj, "posts": page_obj.object_list})
    return TemplateResponse(request, "socialnotpolymorphic/list.html", ctx)
