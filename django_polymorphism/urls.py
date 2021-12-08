"""django_polymorphism URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from socialpolymorphic import views as socialpolymorphic_views

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("admin/", admin.site.urls),
    path("socialnotpolymorphic/", include("socialnotpolymorphic.urls")),
    path("socialconcrete/", include("socialconcrete.urls")),
    path("socialonetoone/", include("socialonetoone.urls")),
    path("socialonlyone/", include("socialonlyone.urls")),
    path("socialcontenttypes/", include("socialcontenttypes.urls")),
    path(
        "socialpolymorphic/",
        socialpolymorphic_views.post_list,
        name="socialpolymorphic-list",
    ),
    path("socialjson/", include("socialjson.urls")),
    path("socialmodelutils/", include("socialmodelutils.urls")),
    path("", TemplateView.as_view(template_name="home.html")),
]
