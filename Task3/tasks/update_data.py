from app.services.source1 import fetch_data_from_source1
from app.services.source2 import fetch_data_from_source2
from app.db.database import SessionLocal
from app.models.station import Station, FuelPrice
from app.services.cache import set_cache_data


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
                fuel_price = db.query(FuelPrice).filter(FuelPrice.station_id == station.id,
                                                        FuelPrice.fuel_type == fuel_data['fuel_type']).first()
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
