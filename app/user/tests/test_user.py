import pytest
from django.urls import reverse
from user.models import User
pytestmark = pytest.mark.django_db


class TestCreateUser:
    register_url = reverse("auth:register-user")

    def test_create_user(self, api_client):
        data = {"email": "user@ridwanray.com", "password": "12345"}
        response = api_client.post(self.register_url, data)
        assert response.status_code == 200
        user_obj : User = User.objects.get(email=data["email"])
        assert user_obj.check_password(data["password"]) 
        assert user_obj.qr_code is not None

    def test_deny_create_user_duplicate_email(self, api_client, active_user):
        """Deny create user; deplicate email"""
        data = {"email": active_user.email, "password": "simplepass@"}
        response = api_client.post(self.register_url, data)
        assert response.status_code == 400
