from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Categories: films, audio or books"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Genres: comedy, thriller etc"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """***"""

    name = models.TextField()
    description = models.TextField("description", null=True)
    year = models.IntegerField("Год создания", default=1990)
    category = models.ForeignKey(
            Category,
            on_delete=models.SET_NULL,
            )
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL)
    

    def __str__(self):
        return self.name