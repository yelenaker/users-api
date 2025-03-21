from fastapi.testclient import TestClient
from main import app
from src.models.users import UserService
from uuid import uuid4
from datetime import date

client = TestClient(app)
user_service = UserService()

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    new_user = {
        "firstName": "Test",
        "lastName": "User",
        "birthday": "2000-01-01"
    }
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["firstName"] == new_user["firstName"]
    assert data["lastName"] == new_user["lastName"]

def test_get_nonexistent_user():
    response = client.get(f"/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_nonexistent_user():
    user_id = uuid4()
    update_data = {
        "firstName": "Updated",
        "lastName": "User",
        "birthday": "1995-05-05",
        "id": str(user_id)
    }
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_delete_nonexistent_user():
    response = client.delete(f"/users/{uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
