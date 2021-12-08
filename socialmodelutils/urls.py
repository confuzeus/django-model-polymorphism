from django.urls import path

from . import views

app_name = "socialmodelutils"

urlpatterns = [path("", views.post_list, name="list")]
