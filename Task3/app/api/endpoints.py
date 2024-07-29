from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.station import Station
from app.schemas.station import Station as StationSchema, StationCreate

router = APIRouter()

@router.get("/stations/", response_model=List[StationSchema])
def read_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stations = db.query(Station).offset(skip).limit(limit).all()
    return stations

@router.get("/stations/{station_id}/", response_model=StationSchema)
def read_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == station_id).first()
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return station

@router.post("/stations/", response_model=StationSchema)
def create_station(station: StationCreate, db: Session = Depends(get_db)):
    db_station = Station(**station.dict())
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station

@router.put("/stations/{station_id}/", response_model=StationSchema)
def update_station(station_id: int, station: StationCreate, db: Session = Depends(get_db)):
    db_station = db.query(Station).filter(Station.id == station_id).first()
    if db_station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    for key, value in station.dict().items():
        setattr(db_station, key, value)
    db.commit()
    db.refresh(db_station)
    return db_station
