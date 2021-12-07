from django.urls import path

from . import views

app_name = "socialjson"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("create/<int:post_type>/", views.create_post, name="create"),
]
