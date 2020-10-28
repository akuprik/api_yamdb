from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """
    role = serializers.ChoiceField(choices=User.ROLE_LIST)
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    bio = serializers.CharField(default='', allow_blank=True, )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role', )


class EmailSerializer(serializers.Serializer):
    """
    Сериализатор запроса для получения confirmation_code
    """
    email = serializers.EmailField(required=True)


class GetAccessParTokenSerializer(serializers.Serializer):
    """
    Сериализатор запроса токена доступа
    """
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
