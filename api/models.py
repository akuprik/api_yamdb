from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    """
    Модель пользователя с добавленными полями
    и переопределенным email, требуется как уникальное,
    по нему идентифицируется пользователь
    """
    email = models.EmailField(unique=True, null=False)
    ROLE_LIST = (
        ('user', 'Простой пользователь'),
        ('moderator', 'Пользователь для модерации'),
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
    genre = models.ManyToManyField(Genre, blank=True, related_name="genres",)
    description = models.TextField('description', null=True)
    year = models.PositiveIntegerField('year')


class Review(models.Model):
    """Создание модели Review"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews',
    )
    text = models.TextField(
        'text',
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='score',
        validators=[
            MinValueValidator(1, message='Min value 1',),
            MaxValueValidator(10, message='Max value 10',)
        ],
        null=False,
    )
    pub_date = models.DateTimeField(
        'Date of publication',
        auto_now_add=True,
    )


class Comment(models.Model):
    """Создание модели Comment"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
    )
    text = models.TextField(
        'text',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Date of publication',
        auto_now_add=True,
        db_index=True,
    )
