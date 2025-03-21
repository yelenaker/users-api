from uuid import UUID, uuid4
from pydantic import BaseModel, field_validator
from datetime import date
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User(BaseModel):
    id: UUID
    firstName: str
    lastName: str
    birthday: date

    @field_validator("firstName", "lastName")
    @classmethod
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Name fields cannot be empty")
        return value

    def __init__(self, **data):
        if "id" not in data or data["id"] is None:
            data["id"] = uuid4()
        super().__init__(**data)

class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
            cls._instance.users = []
            cls._instance._load_test_users()
        return cls._instance

    def _load_test_users(self):
        """Автоматично додає тестових користувачів при запуску сервера."""
        self.users = [
            User(firstName="Alice", lastName="Johnson", birthday=date(1990, 5, 17)),
            User(firstName="Bob", lastName="Smith", birthday=date(1985, 8, 25)),
            User(firstName="Charlie", lastName="Brown", birthday=date(1992, 3, 10)),
        ]
        logger.info(f"Test users added: {self.users}")

    def create_user(self, user: User) -> User:
        if any(existing_user.id == user.id for existing_user in self.users):
            raise ValueError("User with this ID already exists")
        self.users.append(user)
        return user

    def get_users(self) -> List[User]:
        return self.users

    def get_user(self, user_id: UUID) -> Optional[User]:
        user = next((user for user in self.users if user.id == user_id), None)
        return user

    def update_user(self, user_id: UUID, updated_user: User) -> Optional[User]:
        for idx, user in enumerate(self.users):
            if user.id == user_id:
                self.users[idx] = updated_user
                return updated_user
        return None

    def delete_user(self, user_id: UUID) -> bool:
        for idx, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[idx]
                return True
        return False

def get_user_service() -> UserService:
    return UserService()
