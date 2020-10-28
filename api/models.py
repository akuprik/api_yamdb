from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


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
