from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    GetConfirmCodeView,
    GetAuthPairToken
    )

router = DefaultRouter()
router.register('users', UserViewSet, basename='PostViewSet')


urlpatterns = [
    path('v1/auth/email/', GetConfirmCodeView.as_view(), name='confirmation_code'),
    path('v1/auth/token/', GetAuthPairToken.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('v1/', include(router.urls)),

    ]
