from sqlalchemy import Column, String, Date
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import date
from pydantic import BaseModel, ConfigDict
from src.db.database import Base

# SQLAlchemy модель
class User(Base):
    __tablename__ = "users"  # Исправил на tablename

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)

# Pydantic модели

# ✅ для входа
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    birthday: date

# ✅ для обновления
class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    birthday: date

# ✅ для ответа
class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    birthday: date

    model_config = ConfigDict(from_attributes=True)

# Сервис для взаимодействия с базой
class UserService:
    def __init__(self, db: Session):  # Исправил init на __init__
        self.db = db

    def get_users(self):
        return self.db.query(User).all()

    def get_user(self, user_id: str):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user_data: UserCreate):
        new_user = User(**user_data.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id: str, user_data: UserUpdate):
        user = self.get_user(user_id)
        if not user:
            return None
        for field, value in user_data.dict().items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: str):
        user = self.get_user(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

# Фабрика для сервиса
def get_user_service(db: Session):
    return UserService(db)
