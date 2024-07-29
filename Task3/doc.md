### Документация проекта

## Описание проекта

Этот проект представляет собой сервер-посредник, который собирает информацию с нескольких источников, объединяет, модифицирует и кэширует данные, а затем предоставляет их клиентам по запросу. Основная цель - предоставлять информацию об автозаправочных станциях (АЗС), включая их местоположение, адреса, услуги, изображения и цены на топливо.

## Технологический стек

- **Язык программирования**: Python 3
- **Веб-фреймворк**: FastAPI
- **ORM**: SQLAlchemy
- **База данных**: PostgreSQL
- **Кэширование**: Redis
- **Асинхронные задачи**: Celery
- **Инструменты для тестирования**: Pytest

## Установка и запуск

### Требования

- Python 3.8+
- PostgreSQL
- Redis

### Установка зависимостей

Установите зависимости с помощью pip:

```bash
pip install -r requirements.txt
```

### Настройка окружения

Создайте файл `.env` в корне вашего проекта и добавьте следующие переменные окружения:

```dotenv
# Development Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=name
DB_USER=user
DB_PASS=password

# Test Database
DB_HOST_TEST=localhost
DB_PORT_TEST=5432
DB_NAME_TEST=test_name
DB_USER_TEST=test_user
DB_PASS_TEST=test_password

# Redis URL
REDIS_URL=redis://localhost:6379/0
```

### Миграция базы данных

Создайте и примените миграции базы данных:

```bash
alembic upgrade head
```

### Запуск приложения

Запустите приложение FastAPI:

```bash
uvicorn app.main:app --reload
```

### Запуск Celery Worker

Запустите Celery worker для обработки асинхронных задач:

```bash
celery -A app.celery_app worker --loglevel=info
```

### Запуск тестов

Запустите тесты с помощью pytest:

```bash
pytest
```

## Структура проекта

- `app/`
  - `api/`: Маршруты API
  - `core/`: Основные настройки и конфигурации
  - `db/`: Настройки базы данных и модели
  - `schemas/`: Pydantic-схемы для валидации данных
  - `services/`: Логика работы с внешними источниками
  - `tasks/`: Асинхронные задачи Celery
  - `main.py`: Точка входа в приложение

## Пример API

### Получить список всех АЗС

**GET** `/stations/`

Ответ:

```json
[
    {
        "id": 1,
        "name": "Станция 404",
        "latitude": 40.0,
        "longitude": -70.0,
        "address": "г.Казань ул.Красной позиции 6к3",
        "services": ["Запрвка"],
        "images": ["http://example.com/image.jpg"],
        "fuel_prices": [
            {
                "fuel_type": "Бензин_98",
                "price": 50,
                "currency": "РУБ"
            }
        ]
    }
]
```

### Получить информацию об АЗС по ID

**GET** `/stations/{station_id}/`

Ответ:

```json
{
    "id": 1,
    "name": "Станция 404",
    "latitude": 40.0,
    "longitude": -70.0,
    "address": "г.Казань ул.Красной позиции 6к3",
    "services": ["Запрвка"],
    "images": ["http://example.com/image.jpg"],
    "fuel_prices": [
        {
            "fuel_type": "Бензин_98",
            "price": 50,
            "currency": "РУБ"
        }
    ]
}
```

### Создать новую АЗС

**POST** `/stations/`

Тело запроса:

```json
{
    "name": "Станция 228",
    "latitude": 41.0,
    "longitude": -71.0,
    "address": "г.Казань ул.Дружбы 14",
    "services": ["Кафе"],
    "images": ["http://example.com/new_image.jpg"]
}
```

Ответ:

```json
{
    "id": 2,
    "name": "Станция 228",
    "latitude": 41.0,
    "longitude": -71.0,
    "address": "г.Казань ул.Дружбы 14",
    "services": ["Кафе"],
    "images": ["http://example.com/new_image.jpg"],
    "fuel_prices": []
}
```

### Обновить информацию об АЗС

**PUT** `/stations/{station_id}/`

Тело запроса:

```json
{
    "name": "Станция 200",
    "latitude": 42.0,
    "longitude": -72.0,
    "address": "г.Казань ул.Красной позиции 6к3",
    "services": ["Заправка"],
    "images": ["http://example.com/updated_image.jpg"]
}
```

Ответ:

```json
{
    "id": 1,
    "name": "Станция 200",
    "latitude": 42.0,
    "longitude": -72.0,
    "address": "г.Казань ул.Красной позиции 6к3",
    "services": ["Заправка"],
    "images": ["http://example.com/updated_image.jpg"],
    "fuel_prices": [
        {
            "fuel_type": "Бензин_98",
            "price": 68,
            "currency": "РУБ"
        }
    ]
}
```

### Удалить АЗС

**DELETE** `/stations/{station_id}/`

Ответ:

```json
{
    "detail": "Station deleted successfully"
}
```

## Асинхронные задачи

### Обновление данных из внешних источников

Асинхронная задача `update_data` обновляет данные АЗС из двух внешних источников и кэширует их в Redis. Задача выполняется периодически с помощью Celery.

```python
# tasks/update_data.py
from app.services import fetch_data_from_source1
from app.services import fetch_data_from_source2
from app.db.database import SessionLocal
from app.models.station import Station, FuelPrice
from app.services import set_cache_data

def update_data():
    db = SessionLocal()

    source1_data = fetch_data_from_source1()
    source2_data = fetch_data_from_source2()

    # Обработка и сохранение данных из Источника 1
    for station_data in source1_data:
        station = db.query(Station).filter(Station.id == station_data['id']).first()
        if not station:
            station = Station(id=station_data['id'])
        station.name = station_data['name']
        station.latitude = station_data['latitude']
        station.longitude = station_data['longitude']
        station.address = station_data['address']
        station.services = station_data['services']
        station.images = station_data['images']
        db.add(station)
    
    # Обработка и сохранение данных из Источника 2
    for station_data in source2_data:
        station = db.query(Station).filter(Station.id == station_data['id']).first()
        if station:
            for fuel_data in station_data['fuel_prices']:
                fuel_price = db.query(FuelPrice).filter(FuelPrice.station_id == station.id, FuelPrice.fuel_type == fuel_data['fuel_type']).first()
                if not fuel_price:
                    fuel_price = FuelPrice(station_id=station.id, fuel_type=fuel_data['fuel_type'])
                fuel_price.price = fuel_data['price']
                fuel_price.currency = fuel_data['currency']
                db.add(fuel_price)

    db.commit()

    # Кэширование данных
    stations = db.query(Station).all()
    for station in stations:
        set_cache_data(f"station:{station.id}", station.json())

    db.close()
```

## Тестирование

Тесты используют тестовую базу данных для предотвращения влияния на рабочие данные.

```python
# test.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.models.station import Station, FuelPrice
from app.schemas import StationCreate, FuelPriceCreate
from app.core.config import settings

# Создание тестового движка базы данных
SQLALCHEMY_DATABASE_URL_TEST = settings.DATABASE_TEST_URL
engine_test = create_engine(SQLALCHEMY_DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# Создание всех таблиц в тестовой базе данных
Base.metadata.create_all(bind=engine_test)

# Переопределение зависимости get_db для тестов
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    # Заполнение тестовой базы данных начальными данными
    db = TestingSessionLocal()
    station = Station(id=1, name="Test Station", latitude=40.0, longitude=-70.0, address="123 Test St", services=["car_w

ash"], images=["http://example.com/image.jpg"])
    db.add(station)
    db.commit()
    db.refresh(station)
    
    fuel_price = FuelPrice(station_id=1, fuel_type="Petrol", price=1.5, currency="USD")
    db.add(fuel_price)
    db.commit()
    db.refresh(fuel_price)

    yield db

    # Удаление данных после тестов
    Base.metadata.drop_all(bind=engine_test)

def test_read_stations(test_db):
    response = client.get("/stations/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == "Test Station"

def test_read_station(test_db):
    response = client.get("/stations/1/")
    assert response.status_code == 200
    assert response.json()['name'] == "Test Station"

def test_create_station(test_db):
    new_station = {
        "name": "New Station",
        "latitude": 41.0,
        "longitude": -71.0,
        "address": "456 New St",
        "services": ["wifi"],
        "images": ["http://example.com/new_image.jpg"]
    }
    response = client.post("/stations/", json=new_station)
    assert response.status_code == 200
    assert response.json()['name'] == "New Station"

def test_update_station(test_db):
    updated_station = {
        "name": "Updated Station",
        "latitude": 42.0,
        "longitude": -72.0,
        "address": "789 Updated St",
        "services": ["restaurant"],
        "images": ["http://example.com/updated_image.jpg"]
    }
    response = client.put("/stations/1/", json=updated_station)
    assert response.status_code == 200
    assert response.json()['name'] == "Updated Station"
    assert response.json()['services'] == ["restaurant"]

def test_read_non_existent_station(test_db):
    response = client.get("/stations/999/")
    assert response.status_code == 404
```

## Заключение

Этот проект предоставляет масштабируемый и эффективный способ объединения и предоставления данных о АЗС. Использование FastAPI, SQLAlchemy, Celery и Redis обеспечивает высокую производительность и надежность.