from django import template

from socialpolymorphic import models

register = template.Library()


@register.simple_tag()
def get_post_type(post):
    post_type = None

    if isinstance(post, models.TextPost):
        post_type = "text"
    elif isinstance(post, models.YoutubeEmbedPost):
        post_type = "youtube"
    elif isinstance(post, models.ImagePost):
        post_type = "image"
    elif isinstance(post, models.URLPost):
        post_type = "url"

    return post_type
