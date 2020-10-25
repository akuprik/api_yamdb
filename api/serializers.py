from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .models import Title, Review, Comment, User, Category, Genre


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """
    class Meta:
        model = User
        fields = '__all__'


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для Title"""

    class Meta:
        fields = '__all__'
        model = Title


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
