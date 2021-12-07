import random
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from faker import Faker

from socialnotpolymorphic import models as socialnotpolymorphic_models
from socialconcrete import models as socialconcrete_models
from socialonetoone import models as socialonetoone_models
from socialonlyone.models import Post as OneModelPost
from socialcontenttypes import models as socialcontenttypes_models
from socialpolymorphic import models as socialpolymorphic_models
from socialjson.models import Post as SocialJsonPost

User = get_user_model()

fake = Faker()

YOUTUBE_IDS = [
    "RgzLnmTaCAU",
    "uU3AIBmXF1o",
    "0U-zpEk6KlI",
    "_qHiCIKdgLc",
    "ffcitRgiNDs",
    "FgjPQQeTh1w",
    "0e3GPea1Tyg",
    "L0nFX5hKJOk",
    "WgqQo5LmW4k",
    "QN1uygzp56s",
    "SmOrhq_m0ZI",
    "qY3L1bPNBAw",
    "IgYs_NDyaLs",
    "q_HNcBjHlPY",
    "ao2Jfm35XeE",
    "7kwAPr5G6WA",
    "qgY9RYTO7Nw",
    "VcOSUOpACq0",
    "xhxo2oXRiio",
    "59bdqLHHqLo",
    "UxBc-dEAsbs",
    "kzxQgrA7MLg",
    "k75NylpmfcM",
    "hIyEAZlWENs",
    "j9J7cjGU_jM",
    "ZNuZ_NEoGWs",
    "rYLHFMjNZjo",
    "eJlBL8pIY2k",
    "QQ7MimTj2vg",
    "4jtbe0I1e1c",
    "_4kHxtiuML0",
    "JI3AhUgWGDY",
    "QVgXNSuo-PI",
    "xlAogwQakRI",
    "Q8SJC-0VjzI",
    "qMHutS8Yo8I",
    "fxSn0J7qfHs",
    "N6zrNBVVoCY",
    "f6yhsqGp-yk",
    "LXeVrypKoyI",
]


def get_random_image_path():
    return random.choice(list(settings.DUMMY_IMAGE_REPOSITORY.iterdir()))


class Command(BaseCommand):
    def _create_users(self, count=100):
        self.stdout.write(f"Creating {count} users.")

        def create_user():
            User.objects.create(username=fake.user_name(), email=fake.ascii_email())

        for _ in range(count):
            create_user()
        self.stdout.write(self.style.SUCCESS("Success!"))

    def _create_one_to_one_posts(self):
        self.stdout.write("Creating one to one posts.")

        for user in User.objects.all():
            text_post = socialonetoone_models.TextPost.objects.create(
                body=fake.paragraph()
            )
            socialonetoone_models.Post.objects.create(
                user=user, title=fake.sentence(), text_post=text_post
            )

            youtube_post = socialonetoone_models.YoutubeEmbedPost.objects.create(
                video_id=random.choice(YOUTUBE_IDS)
            )
            socialonetoone_models.Post.objects.create(
                user=user, title=fake.sentence(), youtube_post=youtube_post
            )

            random_image_path = get_random_image_path()
            with random_image_path.open("rb") as image_file:
                django_image_file = ImageFile(
                    file=image_file, name=random_image_path.name
                )
                image_post = socialonetoone_models.ImagePost.objects.create(
                    image=django_image_file
                )
                socialonetoone_models.Post.objects.create(
                    user=user, title=fake.sentence(), image_post=image_post
                )

            url_post = socialonetoone_models.URLPost.objects.create(url=fake.uri())
            socialonetoone_models.Post.objects.create(
                user=user, title=fake.sentence(), url_post=url_post
            )

        self.stdout.write(self.style.SUCCESS("Success!"))

    def _create_json_posts(self):
        self.stdout.write("Creating JSONField posts.")

        for user in User.objects.all():
            SocialJsonPost.objects.create(
                user=user,
                title=fake.sentence(),
                post_type=SocialJsonPost.TEXT_POST_TYPE,
                data={"text_body": fake.paragraph()},
            )

            SocialJsonPost.objects.create(
                user=user,
                title=fake.sentence(),
                data={"video_id": random.choice(YOUTUBE_IDS)},
                post_type=SocialJsonPost.YOUTUBE_POST_TYPE,
            )

            random_image_path = get_random_image_path()
            destination_path = settings.MEDIA_ROOT / user.username
            destination_path.mkdir(parents=True, exist_ok=True)
            shutil.copy(random_image_path, destination_path)
            SocialJsonPost.objects.create(
                user=user,
                title=fake.sentence(),
                data={"image": f"{settings.MEDIA_URL}{user}/{random_image_path.name}"},
                post_type=SocialJsonPost.IMAGE_POST_TYPE,
            )

            SocialJsonPost.objects.create(
                user=user,
                title=fake.sentence(),
                data={"url": fake.uri()},
                post_type=SocialJsonPost.URL_POST_TYPE,
            )

        self.stdout.write(self.style.SUCCESS("Success!"))

    def _create_one_model_posts(self):
        self.stdout.write("Creating one model posts.")

        for user in User.objects.all():
            OneModelPost.objects.create(
                user=user,
                title=fake.sentence(),
                text_body=fake.paragraph(),
                post_type=OneModelPost.TEXT_POST_TYPE,
            )

            OneModelPost.objects.create(
                user=user,
                title=fake.sentence(),
                youtube_video_id=random.choice(YOUTUBE_IDS),
                post_type=OneModelPost.YOUTUBE_POST_TYPE,
            )

            random_image_path = get_random_image_path()
            with random_image_path.open("rb") as image_file:
                django_image_file = ImageFile(
                    file=image_file, name=random_image_path.name
                )
                OneModelPost.objects.create(
                    user=user,
                    title=fake.sentence(),
                    image=django_image_file,
                    post_type=OneModelPost.IMAGE_POST_TYPE,
                )

            OneModelPost.objects.create(
                user=user,
                title=fake.sentence(),
                url=fake.uri(),
                post_type=OneModelPost.URL_POST_TYPE,
            )

        self.stdout.write(self.style.SUCCESS("Success!"))

    def _create_polymorphic_posts(self):
        self.stdout.write("Creating polymorphic posts")

        for user in User.objects.all():

            socialpolymorphic_models.TextPost.objects.create(
                user=user, title=fake.sentence(), body=fake.paragraph()
            )

            socialpolymorphic_models.YoutubeEmbedPost.objects.create(
                user=user, title=fake.sentence(), video_id=random.choice(YOUTUBE_IDS)
            )

            random_image_path = get_random_image_path()
            with random_image_path.open("rb") as image_file:
                django_image_file = ImageFile(
                    file=image_file, name=random_image_path.name
                )
                socialpolymorphic_models.ImagePost.objects.create(
                    user=user, title=fake.sentence(), image=django_image_file
                )

            socialpolymorphic_models.URLPost.objects.create(
                user=user, title=fake.sentence(), url=fake.uri()
            )

        self.stdout.write(self.style.SUCCESS("Success!"))

    def _create_concrete_posts(self):
        self.stdout.write("Creating concrete posts.")

        for user in User.objects.all():

            socialconcrete_models.TextPost.objects.create(
                user=user, title=fake.sentence(), body=fake.paragraph()
            )

            socialconcrete_models.YoutubeEmbedPost.objects.create(
                user=user, title=fake.sentence(), video_id=random.choice(YOUTUBE_IDS)
            )

            random_image_path = get_random_image_path()
            with random_image_path.open("rb") as image_file:
                django_image_file = ImageFile(
                    file=image_file, name=random_image_path.name
                )
                socialconcrete_models.ImagePost.objects.create(
                    user=user, title=fake.sentence(), image=django_image_file
                )

            socialconcrete_models.URLPost.objects.create(
                user=user, title=fake.sentence(), url=fake.uri()
            )

        self.stdout.write(self.style.SUCCESS("Success!"))

    def _create_content_types_posts(self):
        self.stdout.write("Creating content types posts.")

        for user in User.objects.all():

            text_post = socialcontenttypes_models.TextPost.objects.create(
                body=fake.paragraph()
            )
            text_post_type = ContentType.objects.get_for_model(
                socialcontenttypes_models.TextPost
            )
            socialcontenttypes_models.Post.objects.create(
                user=user,
                title=fake.sentence(),
                post_content_type=text_post_type,
                post_object_id=text_post.pk,
            )

            youtube_post = socialcontenttypes_models.YoutubeEmbedPost.objects.create(
                video_id=random.choice(YOUTUBE_IDS)
            )

            youtube_post_type = ContentType.objects.get_for_model(
                socialcontenttypes_models.YoutubeEmbedPost
            )

            socialcontenttypes_models.Post.objects.create(
                user=user,
                title=fake.sentence(),
                post_content_type=youtube_post_type,
                post_object_id=youtube_post.pk,
            )

            random_image_path = get_random_image_path()
            with random_image_path.open("rb") as image_file:
                django_image_file = ImageFile(
                    file=image_file, name=random_image_path.name
                )
                image_post = socialcontenttypes_models.ImagePost.objects.create(
                    image=django_image_file
                )
                image_post_type = ContentType.objects.get_for_model(
                    socialcontenttypes_models.YoutubeEmbedPost
                )

                socialcontenttypes_models.Post.objects.create(
                    user=user,
                    title=fake.sentence(),
                    post_content_type=image_post_type,
                    post_object_id=image_post.pk,
                )

            url_post = socialcontenttypes_models.URLPost.objects.create(url=fake.uri())

            url_post_type = ContentType.objects.get_for_model(
                socialcontenttypes_models.YoutubeEmbedPost
            )

            socialcontenttypes_models.Post.objects.create(
                user=user,
                title=fake.sentence(),
                post_content_type=url_post_type,
                post_object_id=url_post.pk,
            )

        self.stdout.write(self.style.SUCCESS("Success!"))

    def _create_not_polymorphic_posts(self):
        self.stdout.write("Creating posts without polymorphism.")

        for user in User.objects.all():

            socialnotpolymorphic_models.TextPost.objects.create(
                user=user, title=fake.sentence(), body=fake.paragraph()
            )

            socialnotpolymorphic_models.YoutubeEmbedPost.objects.create(
                user=user, title=fake.sentence(), video_id=random.choice(YOUTUBE_IDS)
            )

            random_image_path = get_random_image_path()
            with random_image_path.open("rb") as image_file:
                django_image_file = ImageFile(
                    file=image_file, name=random_image_path.name
                )
                socialnotpolymorphic_models.ImagePost.objects.create(
                    user=user, title=fake.sentence(), image=django_image_file
                )

            socialnotpolymorphic_models.URLPost.objects.create(
                user=user, title=fake.sentence(), url=fake.uri()
            )

        self.stdout.write(self.style.SUCCESS("Success!"))

    def handle(self, *args, **options):
        self._create_users()
        self._create_not_polymorphic_posts()
        self._create_concrete_posts()
        self._create_one_to_one_posts()
        self._create_one_model_posts()
        self._create_content_types_posts()
        self._create_polymorphic_posts()
        self._create_json_posts()
