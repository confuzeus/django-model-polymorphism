# Django polymorphism tutorial

This repo contains code for a tutorial on my blog:

[https://confuzeus.com/hub/django-web-framework/model-polymorphism](https://confuzeus.com/hub/django-web-framework/model-polymorphism)

## Usage guide

Setup the project:

`pip install -r requirements.txt`

`python manage.py migrate`

Change the setting variable named `DUMMY_IMAGE_REPOSITORY`

This variable needs to point to a directory containing images which will be used to populate `ImageField`s.

`python manage.py init_posts`