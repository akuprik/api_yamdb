from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.db.models import Avg

from .models import Title, Review, Comment, User, Category, Genre


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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Category"""

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для Genre"""

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для Title"""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Review"""

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Comment"""

    class Meta:
        fields = '__all__'
        model = Comment
