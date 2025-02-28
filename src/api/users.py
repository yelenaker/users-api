from fastapi import APIRouter, Depends
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
