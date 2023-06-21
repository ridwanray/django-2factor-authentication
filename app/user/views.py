from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import User
from .serializers import (
    VerifyOTPSerializer,
    UserSerializer,
    LoginSerialiazer,
)


class VerityOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_info: dict = serializer.save()
        return Response(login_info,status=200)


class  UserProfileView(generics.GenericAPIView):
    """Returns user profile details"""
    permission_classes =  [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response({"success": True, "data": serializer.data}, status=200)



class LoginView(generics.GenericAPIView):
    """Login with email and password"""

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerialiazer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "success": True,
                "user": user.id,
                "message": "Login Successful. Proceed to 2FA",
            },
            status=200,
        )


class CreateUserView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        user: User = self.request.user
        if user.is_admin:
            return super().get_queryset().all()
        return super().get_queryset().filter(id=user.id)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "message": "Registration Successful!"}, status=200
        )
