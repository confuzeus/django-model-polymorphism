from django import template

register = template.Library()


@register.simple_tag()
def get_actual_post(post):
    data = {}

    try:
        data["obj"] = post.textpost
        data["post_type"] = "text"
    except post.DoesNotExist:
        try:
            data["obj"] = post.youtubeembedpost
            data["post_type"] = "youtube"
        except post.DoesNotExist:
            try:
                data["obj"] = post.urlpost
                data["post_type"] = "url"
            except post.DoesNotExist:
                try:
                    data["obj"] = post.imagepost
                    data["post_type"] = "image"
                except post.DoesNotExist as e:
                    raise post.DoesNotExist from e

    return data
