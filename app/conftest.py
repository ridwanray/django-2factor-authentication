import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from user.tests.factories import UserFactory

register(UserFactory)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def active_user(db, user_factory):
    return user_factory.create(is_active=True)

@pytest.fixture
def inactive_user(db, user_factory):
    user = user_factory.create(is_active=False)
    return user

@pytest.fixture
def auth_user_password()->str:
    '''returns user password to be used in authentication'''
    return 'passer@@@111'