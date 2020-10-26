from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet


v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet)
v1_router.register('genres', GenresViewSet)
v1_router.register('tetles', TitlesViewSet)


urlpatterns = [
    path('api/', include('api.urls')),
]
