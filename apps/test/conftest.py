import pytest

from apps.test.test_sql_app import client


@pytest.fixture(scope="module")
def test_client_app():
    yield client


@pytest.fixture(scope="session")
def data_user():
    return {
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "string",
        "email": "user@exemple.com",
    }


@pytest.fixture(scope="session")
def data_user_update():
    return {
        "first_name": "string",
        "last_name": "string",
        "email": "user@exemple.com"
    }
