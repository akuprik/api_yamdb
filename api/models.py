from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser

<<<<<<< HEAD
=======

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


>>>>>>> 21de50af490b65b3dcb6765726d74d48b104d851
User = get_user_model()


class Category(models.Model):
    """Categories: films, audio or books"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

<<<<<<< HEAD
    def __str__(self):
        return self.name

=======
>>>>>>> 21de50af490b65b3dcb6765726d74d48b104d851

class Genre(models.Model):
    """Genres: comedy, thriller etc"""

    name = models.TextField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

<<<<<<< HEAD
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
=======

class Title(models.Model):
    """Модель Title"""

    name = models.TextField('name')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='titles')
    genre = models.ManyToManyField(Genre)
    description = models.TextField('description', null=True)
    year = models.IntegerField('year')


class Review(models.Model):
    """Модель Review"""

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('text')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField('score', null=True)
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True)


class Comment(models.Model):
    """Модель Comment"""

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('text')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True, db_index=True)
>>>>>>> 21de50af490b65b3dcb6765726d74d48b104d851
