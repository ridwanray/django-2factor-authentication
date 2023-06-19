from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (CustomObtainTokenPairSerializer)


class CustomObtainTokenPairView(TokenObtainPairView):
    """Authentice with phone number and password"""
    serializer_class = CustomObtainTokenPairSerializer