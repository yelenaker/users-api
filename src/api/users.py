from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.models.users import User
from src.models.users import get_user_service, UserService

router = APIRouter()

@router.get("/users", response_model=List[User])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

@router.post("/users", response_model=User)
def create_user(user: User, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user_data: User, service: UserService = Depends(get_user_service)):
    updated_user = service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}")
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
