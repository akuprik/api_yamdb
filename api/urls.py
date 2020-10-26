from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserViewSet, GetConfirmCodeView,
    GetAuthPairToken, TitleViewSet,
    ReviewViewSet, CommentViewSet,
    CategoryViewSet, GenreViewSet
)


v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('reviews', ReviewViewSet)
v1_router.register('comments', CommentViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', GetConfirmCodeView.as_view(), name='confirmation_code'),
    path('v1/auth/token/', GetAuthPairToken.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
