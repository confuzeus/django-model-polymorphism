# Generated by Django 3.2.9 on 2021-12-04 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import socialconcrete.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=155)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="socialconcrete_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_added"],
            },
        ),
        migrations.CreateModel(
            name="ImagePost",
            fields=[
                (
                    "post_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="socialconcrete.post",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=socialconcrete.models.user_directory_path
                    ),
                ),
            ],
            bases=("socialconcrete.post",),
        ),
        migrations.CreateModel(
            name="TextPost",
            fields=[
                (
                    "post_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="socialconcrete.post",
                    ),
                ),
                ("body", models.TextField(max_length=10000)),
            ],
            bases=("socialconcrete.post",),
        ),
        migrations.CreateModel(
            name="URLPost",
            fields=[
                (
                    "post_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="socialconcrete.post",
                    ),
                ),
                ("url", models.URLField()),
            ],
            bases=("socialconcrete.post",),
        ),
        migrations.CreateModel(
            name="YoutubeEmbedPost",
            fields=[
                (
                    "post_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="socialconcrete.post",
                    ),
                ),
                ("video_id", models.CharField(max_length=24)),
            ],
            bases=("socialconcrete.post",),
        ),
    ]
