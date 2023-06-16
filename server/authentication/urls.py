from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)

from authentication.views import UserRegisterApiView, UserTgCheckerApiView, UserUpdateApiView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('users/register/', UserRegisterApiView.as_view(), name="user_register"),
    path("users/update/", UserUpdateApiView.as_view(), name="user_update"),
    path("users/check_tg_user/", UserTgCheckerApiView.as_view(), name="check_tg_user"),
]
