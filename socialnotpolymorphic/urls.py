from django.urls import path

from . import views

app_name = "socialnotpolymorphic"

urlpatterns = [path("", views.post_list, name="list")]
