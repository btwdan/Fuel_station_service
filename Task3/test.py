import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base, get_db
from app.models.station import Station, FuelPrice
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
    station = Station(id=1, name="Test Station", latitude=40.0, longitude=-70.0, address="123 Test St",
                      services=["car_wash"], images=["http://example.com/image.jpg"])
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
