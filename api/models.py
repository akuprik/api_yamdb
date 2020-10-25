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
    #category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    description = models.TextField("description", null=True)
    year = models.IntegerField()


class Review(models.Model):
    """***"""

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(null=True)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)


class Comment(models.Model):
    """***"""

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)