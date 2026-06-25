from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

urlpatterns = [
    path("register/",RegisterView.as_view()),
    path("login/",TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("delete-account/" , DeleteAccountView.as_view()),
    path("change-password/" , ChangePasswordView.as_view()),
    path("update-profile/" , UpdateProfileView.as_view()),
    path("reset-password/request/" , ResetPasswordRequestView.as_view()),
    path("reset-password/confirm/" , ResetPasswordConfirmView.as_view())
]
