from django.contrib import admin

from . import models

admin.site.register(models.Post)
admin.site.register(models.TextPost)
admin.site.register(models.YoutubeEmbedPost)
admin.site.register(models.ImagePost)
admin.site.register(models.URLPost)
