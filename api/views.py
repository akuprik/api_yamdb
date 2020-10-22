import django_filters.rest_framework
from django.shortcuts import get_object_or_404, render
from rest_framework import filters, generics, status, viewsets
from rest_framework.viewsets import ViewSetMixin

from .models import Categories, Genres, Titles


class CategoriesViewSet(viewsets.ModelViewSet):
    pass


class GenresViewSet(viewsets.ModelViewSet):
    pass


class TitlesViewSet(viewsets.TitleViewSet):
    pass
