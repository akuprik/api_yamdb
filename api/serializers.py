# почистить и сгруппировать импорты

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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Category"""

    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для Genre"""

    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializer_get(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)


    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score')).get('score__avg')
        if rating is None:
            return 0
        return rating


class TitleSerializer_post(serializers.ModelSerializer):


    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True,
        )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score')).get('score__avg')
        if rating is None:
            return 0
        return rating



class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Review"""

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (
            request.method != 'PATCH' and
            Review.objects.filter(title=title, author=request.user).exists()
        ):
            raise serializers.ValidationError('Score already exists')
        return data

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'title': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Comment"""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
