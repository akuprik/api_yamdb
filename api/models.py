from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Categories: films, audio or books"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Genres: comedy, thriller etc"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    """***"""

    name = models.TextField()
    description = models.TextField("description", null=True)
    year = models.DateTimeField(
        "Год создания", auto_now_add=True
    )
    category = models.ForeignKey(
            Category,
            on_delete=models.SET_NULL,
            )

    def __str__(self):
        return self.name