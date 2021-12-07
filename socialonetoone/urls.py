from django.urls import path

from . import views

app_name = "socialonetoone"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("create/<str:post_type>/", views.create_post, name="create"),
]
