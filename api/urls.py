from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    GetConfirmCodeView,
    GetAuthPairToken,
    CategoryViewSet, 
    GenreViewSet, 
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
    )


v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('reviews', ReviewViewSet)
v1_router.register('comments', CommentViewSet)
v1_router.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet)
v1_router.register(r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments', CommentViewSet)


urlpatterns = [
    path('v1/auth/email/', GetConfirmCodeView.as_view(), name='confirmation_code'),
    path('v1/auth/token/', GetAuthPairToken.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(v1_router.urls)),
    ]
