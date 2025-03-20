from uuid import UUID, uuid4
from pydantic import BaseModel, field_validator
from datetime import date
from typing import List, Optional

class User(BaseModel):
    id: UUID = uuid4()
    firstName: str
    lastName: str
    birthday: date

    @field_validator("firstName", "lastName")
    @classmethod
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Name fields cannot be empty")
        return value

class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
            cls._instance.users = []
        return cls._instance

    def create_user(self, user: User) -> User:
        """Создаёт нового пользователя и добавляет в список."""
        self.users.append(user)
        return user

    def get_users(self) -> List[User]:
        """Возвращает список всех пользователей."""
        return self.users

    def get_user(self, user_id: UUID) -> Optional[User]:
        """Ищет пользователя по ID, иначе вызывает ошибку 404."""
        from fastapi import HTTPException

        user = next((user for user in self.users if user.id == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, user_id: UUID, updated_user: User) -> Optional[User]:
        """Обновляет данные пользователя, если он найден."""
        for idx, user in enumerate(self.users):
            if user.id == user_id:
                self.users[idx] = updated_user
                return updated_user
        return None

    def delete_user(self, user_id: UUID) -> bool:
        """Удаляет пользователя по ID, если он существует."""
        for idx, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[idx]
                return True
        return False

def get_user_service() -> UserService:
    return UserService()