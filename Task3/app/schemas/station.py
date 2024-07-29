from pydantic import BaseModel
from typing import List, Optional

class FuelPriceBase(BaseModel):
    fuel_type: str
    price: float
    currency: str

class FuelPriceCreate(FuelPriceBase):
    pass

class FuelPrice(FuelPriceBase):
    id: int
    station_id: int

    class Config:
        orm_mode = True

class StationBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: str
    services: List[str]
    images: List[str]

class StationCreate(StationBase):
    pass

class Station(StationBase):
    id: int
    fuel_prices: List[FuelPrice] = []

    class Config:
        orm_mode = True
