import pyotp
import pytest


def api_client_with_credentials(token: str, api_client):
    return api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)


def generate_authenticator_otp(user_secret:str)->str:
    """Simulate an authenicator"""
    return pyotp.TOTP(user_secret).now()
