from fastapi import FastAPI
from src.api.users import router as users_router
from src.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)