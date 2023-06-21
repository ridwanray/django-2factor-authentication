from datetime import datetime, timedelta, timezone

import pytest
import time_machine
from django.urls import reverse
from rest_framework import status

from .conftest import generate_authenticator_otp

pytestmark = pytest.mark.django_db


class TestAuthEndpoints:
    login_url = reverse("auth:login")

    def test_user_login(self, api_client, active_user, auth_user_password):
        data = {"email": active_user.email, "password": auth_user_password}
        response = api_client.post(self.login_url, data)
        returned_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert returned_json["user"] == str(active_user.id)
        assert active_user.qr_code is not None

    def test_deny_login_invalid_credentials(self, api_client, active_user):
        """Invalid credentials"""
        data = {"email": active_user.email, "password": "wrongpass"}
        response = api_client.post(self.login_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deny_login_inactive_user(
        self, api_client, inactive_user, auth_user_password
    ):
        data = {"email": inactive_user.email, "password": auth_user_password}
        response = api_client.post(self.login_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_correct_otp(self, api_client, active_user, auth_user_password):
        # perfrom login attempt
        data = {"email": active_user.email, "password": auth_user_password}
        api_client.post(self.login_url, data)

        # simulate authenticator
        authenicator_code = generate_authenticator_otp(active_user.otp_base32)

        # verify token
        url = reverse("auth:verify-otp")
        verify_payload = {
            "otp": authenicator_code,
            "user_id": str(active_user.id),
        }
        response = api_client.post(url, verify_payload)
        assert response.status_code == 200
        json_resonse = response.json()
        assert "access" in json_resonse
        assert "refresh" in json_resonse

    def test_verify_used_otp(self, api_client, active_user, auth_user_password):
        # perform login attempt
        data = {"email": active_user.email, "password": auth_user_password}
        api_client.post(self.login_url, data)
        active_user.refresh_from_db()

        # mark otp as used
        active_user.login_otp_used = True
        active_user.save()

        # simulate authenticator
        authenicator_code = generate_authenticator_otp(active_user.otp_base32)

        # verify token
        url = reverse("auth:verify-otp")
        verify_payload = {
            "otp": authenicator_code,
            "user_id": str(active_user.id),
        }
        response = api_client.post(url, verify_payload)
        assert response.status_code == 401

    @pytest.mark.parametrize(
        "future_seconds,response_code,",
        [
            (5, 200),
            (10, 200),
            (15, 200),
            (20, 200),
            (25, 200),
            (32, 401),
            (35, 401),
            (40, 401),
        ],
    )
    def test_verify_expired_otp(
        self, future_seconds, response_code, api_client, active_user, auth_user_password
    ):
        # perform login attempt
        data = {"email": active_user.email, "password": auth_user_password}
        api_client.post(self.login_url, data)
        active_user.refresh_from_db()

        # simulate authenticator
        authenicator_code = generate_authenticator_otp(active_user.otp_base32)

        # simulate future time
        with time_machine.travel(datetime.now(timezone.utc) + timedelta(seconds=future_seconds)):
            url = reverse("auth:verify-otp")
            verify_payload = {
                "otp": authenicator_code,
                "user_id": str(active_user.id),
            }
            response = api_client.post(url, verify_payload)
            assert response.status_code == response_code

    def test_verify_invalid_otp(self, api_client, active_user, auth_user_password):
        # perform login attempt
        data = {"email": active_user.email, "password": auth_user_password}
        api_client.post(self.login_url, data)

        # simulate authenticator
        authenicator_code = generate_authenticator_otp(active_user.otp_base32)

        # verify token
        url = reverse("auth:verify-otp")
        verify_payload = {
            "otp": f"{authenicator_code}23", #wrong OTP
            "user_id": str(active_user.id),
        }
        response = api_client.post(url, verify_payload)
        assert response.status_code == 401
