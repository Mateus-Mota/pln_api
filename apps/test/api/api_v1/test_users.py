import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from apps import crud


@pytest.fixture(scope="module")
def test_create_user(test_client_app: TestClient, data_user):
    response = test_client_app.post("/auth/sign-up", json=data_user)
    assert response.status_code == 201
    yield response


def test_user_list(test_client_app: TestClient, test_create_user):
    response = test_client_app.get("users")
    assert response.status_code == 404
