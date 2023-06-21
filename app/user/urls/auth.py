from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from ..views import CreateUserView, VerityOTPView, LoginView, UserProfileView

app_name = "auth"
router = DefaultRouter()

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register-user"),
    path("login/", LoginView.as_view(), name="login"),
    path("verity-otp/", VerityOTPView.as_view(), name="verify-otp"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify-token"),
    

    path("", include(router.urls)),
]


