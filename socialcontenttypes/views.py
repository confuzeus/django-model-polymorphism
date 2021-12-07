from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from .models import Post, PostForm


def post_list(request):
    ctx = {}
    paginator = Paginator(Post.objects.all(), 10)
    page_obj = paginator.page(request.GET.get("page", 1))
    ctx.update({"posts": page_obj.object_list, "page_obj": page_obj})
    return TemplateResponse(request, "socialcontenttypes/list.html", ctx)


@login_required
def create_post(request, post_type):
    ctx = {}
    form = None
    kwargs = {"user": request.user, "post_type": post_type}
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, **kwargs)

        if form.is_valid():
            form.save()
            return redirect("socialcontenttypes:list")
    if not form:
        form = PostForm(**kwargs)
    ctx["form"] = form
    return TemplateResponse(request, "create.html", ctx)
