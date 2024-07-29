from fastapi import FastAPI
from app.api import endpoints
from app.db.database import Base, engine

app = FastAPI()

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

# Подключение роутов
app.include_router(endpoints.router)
