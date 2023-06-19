
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access_token = refresh.access_token
        self.user.save_last_login()
        data['refresh'] = str(refresh)
        data['access'] = str(access_token)
        return data

    @classmethod
    def get_token(cls, user: User):
        if not user.verified:
            raise exceptions.AuthenticationFailed(
                _('Account not verified.'), code='authentication')
        token = super().get_token(user)
        token.id = user.id
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token["email"] = user.email
        token["roles"] = user.roles
        return token


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")
        if email:
            user = authenticate(request=self.context.get(
                "request"), username=email.lower().strip(), password=password)

        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")
        attrs["user"] = user
        return attrs

