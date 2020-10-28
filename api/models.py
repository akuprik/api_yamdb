from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    """
    Модель пользователя с добавленными полями
    и переопределенным email, требуется как уникальное,
    по нему идентифицируется пользователь
    """
    email = models.EmailField(unique=True, null=False)
    ROLE_LIST = (
        ('u', 'user'),
        ('m', 'moderator'),
        ('a', 'administrator'),
    )
    role = models.CharField(max_length=1, choices=ROLE_LIST, default='u')
    bio = models.TextField(default='')

    def get_payload(self):
        """
        Полезная нагрузка для формирования confirmation_code
        """
        return {'user_id': self.id, 'email': self.email, 'username': self.username}



class CustomUser(AbstractUser):
    """
    Модель пользователя с добавленными полями
    и переопределенным email, требуется как уникальное,
    по нему идентифицируется пользователь
    """
    email = models.EmailField(unique=True, null=False)
    ROLE_LIST = (
        ('user', 'Простой пользователь'),
        ('moderator', 'Пользовтель для модерации'),
        ('admin', 'Администратор сайта'),
        )
    role = models.CharField(max_length=9, choices=ROLE_LIST, default='user')
    bio = models.TextField(default='')

    def get_payload(self):
        """
        Полезная нагрузка для формирования confirmation_code
        """
        return {'user_id': self.id, 'email': self.email, 'username': self.username}

    class Meta:
        ordering = ("username",)

User = get_user_model()


class Category(models.Model):
    """Categories: films, audio or books"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


class Genre(models.Model):
    """Genres: comedy, thriller etc"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


class Title(models.Model):
    """Модель Title"""

    name = models.TextField('name')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='titles')
    genre = models.ManyToManyField(Genre, blank=True, related_name="genres,")
    description = models.TextField('description', null=True)
    year = models.PositiveIntegerField('year')
    
    def __str__(self):
        return self.name

class Review(models.Model):
    """Модель Review"""

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('text')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveIntegerField('score', null=True)
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True)


class Comment(models.Model):
    """Модель Comment"""

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('text')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True, db_index=True)
