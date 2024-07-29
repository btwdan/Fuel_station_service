from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    services = Column(JSON)
    images = Column(JSON)
    fuel_prices = relationship("FuelPrice", back_populates="station")

class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"))
    fuel_type = Column(String)
    price = Column(Float)
    currency = Column(String)
    station = relationship("Station", back_populates="fuel_prices")
