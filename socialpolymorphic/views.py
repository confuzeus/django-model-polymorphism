from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from .models import Post


def post_list(request):
    ctx = {}
    paginator = Paginator(Post.objects.all(), 10)
    page_obj = paginator.page(request.GET.get("page", 1))
    ctx.update({"posts": page_obj.object_list, "page_obj": page_obj})
    return TemplateResponse(request, "socialpolymorphic/list.html", ctx)
