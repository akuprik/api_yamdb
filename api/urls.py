from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    GetConfirmCodeView,
    GetAuthPairToken,
    CategoriesViewSet, 
    GenresViewSet, 
    TitlesViewSet,
    )


v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet)
v1_router.register('categories/{slug}', CategoriesViewSet)
v1_router.register('genres', GenresViewSet)
v1_router.register('genres/{slug}', GenresViewSet)
v1_router.register('tetles', TitlesViewSet)
v1_router.register('tetles/{titles_id}', TitlesViewSet)
v1_router.register('users', UserViewSet, basename='PostViewSet')


urlpatterns = [
    path('v1/auth/email/', GetConfirmCodeView.as_view(), name='confirmation_code'),
    path('v1/auth/token/', GetAuthPairToken.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(v1_router.urls)),

    ]
