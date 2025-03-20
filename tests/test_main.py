import pytest
from fastapi.testclient import TestClient
from main import app, get_settings
from uuid import uuid4

client = TestClient(app)

@pytest.fixture
def test_user():
    """Фикстура создаёт тестового пользователя и возвращает его ID"""
    user_data = {
        "firstName": "Test",
        "lastName": "User",
        "birthday": "2000-01-01"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201, f"Unexpected response: {response.json()}"
    return response.json()["id"]

def test_root():
    """Проверяет, что корневой маршрут работает"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Users API is running"
    assert data["version"] == get_settings().APPLICATION_VERSION
    assert data["test_mode"] == get_settings().TEST_MODE

def test_get_user(test_user):
    """Проверяет получение пользователя по ID"""
    response = client.get(f"/users/{test_user}")
    assert response.status_code == 200
    data = response.json()
    assert "firstName" in data
    assert "lastName" in data
    assert "birthday" in data

def test_get_non_existent_user():
    """Проверяет получение несуществующего пользователя"""
    fake_uuid = uuid4()
    response = client.get(f"/users/{fake_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_user(test_user):
    """Проверяет обновление пользователя"""
    new_data = {"firstName": "Updated", "lastName": "User", "birthday": "1995-05-05"}

    response = client.put(f"/users/{test_user}", json=new_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

    response = client.get(f"/users/{test_user}")
    updated_user = response.json()
    assert updated_user["firstName"] == new_data["firstName"]
    assert updated_user["lastName"] == new_data["lastName"]
    assert updated_user["birthday"] == new_data["birthday"]