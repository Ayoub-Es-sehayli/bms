import logging
import pytest
from fastapi.testclient import TestClient
from bms import app

logger = logging.getLogger("bms.test.security")
credentials = {
    'username': "test_user",
    'email': "test@test.bms",
    'name': "John Doe",
    'password':"testPassword213"
}

@pytest.fixture
def client():
    return TestClient(app)

def test_can_create_user(client: TestClient):
    try:
        response = client.post("/api/users",
                            json=dict(
                                username= credentials['username'],
                                name= credentials['name'],
                                email= credentials['email']
                            ))
        assert response.status_code == 201

        response = client.post("/api/users",
                            json=dict(
                                username= credentials['username'],
                                name= credentials['name'],
                                email= credentials['email']
                            ))
        assert response.status_code == 200
        assert response.json()['message'] == "User with this username already exists"
    finally:
        # Remove User
        client.delete(f"/api/users/{credentials['username']}")

def test_can_remove_user(client: TestClient):
    # Create User
    response = client.post("/api/users", json=credentials)
    # Remove User
    response = client.delete(f"/api/users/{credentials['username']}")

    assert response.status_code == 200

def test_can_login(client: TestClient):
    try:
        # Create User
        client.post("/api/users",
                            json=dict(
                                username= credentials['username'],
                                name= credentials['name'],
                                email= credentials['email']
                            ))
        response = client.post("/api/users/login",
                            json=dict(
                                username=credentials['username'],
                                password=credentials['password']
                            ))
        user = response.json()

        assert response.status_code == 200
        assert user['username'] == credentials['username']
        assert user['token']
    finally:
        # Remove User
        client.delete(f"/api/users/{credentials['username']}")
