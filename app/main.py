from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schema import Unit, UnitCreate, UnitStatusUpdate
from app.database import engine, Base, get_db
from app.db_models import UnitDB

Base.metadata.create_all(bind=engine)

app = FastAPI()

PREFIXES = {"Ambulance": "AMB", "Firetruck": "FT", "Police" : "PO"}


def generate_callsign(db: Session, unit_type: str) -> str:
    prefix = PREFIXES.get(unit_type)
    if prefix is None:
        raise HTTPException(status_code=400, detail=f"Unknown unit type: {unit_type}")
    callsigns = db.scalars(
        select(UnitDB.callsign).where(UnitDB.callsign.like(f"{prefix}-%"))
    ).all()
    numbers = [int(c.split("-")[1]) for c in callsigns]
    return f"{prefix}-{max(numbers, default=0) + 1}"


@app.get("/")
def root():
    return {"message": "Unit Management API is running"}


@app.get("/api/units", response_model=list[Unit])
def get_units(status: str | None = None, unit_type: str | None = None,station_location: str | None = None,
              db: Session = Depends(get_db)):
    query = select(UnitDB)
    if status is not None:
        query = query.where(UnitDB.status == status)
    if unit_type is not None:
        query = query.where(UnitDB.unit_type == unit_type)
    if station_location is not None:
        query = query.where(UnitDB.station_location == station_location)
    return db.scalars(query).all()


@app.get("/api/units/{unit_id}", response_model=Unit)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.get(UnitDB, unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail=f"Unit {unit_id} not found")
    return unit


@app.post("/api/units", response_model=Unit, status_code=201)
def create_unit(unit_data: UnitCreate, db: Session = Depends(get_db)):
    new_unit = UnitDB(
        callsign=generate_callsign(db, unit_data.unit_type),
        unit_type=unit_data.unit_type,
        status="available",
        station_location=unit_data.station_location,
    )
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit


@app.patch("/api/units/{unit_id}/status", response_model=Unit)
def update_status(unit_id: int, status_update: UnitStatusUpdate,
                  db: Session = Depends(get_db)):
    unit = db.get(UnitDB, unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail=f"Unit {unit_id} not found")
    unit.status = status_update.status.value
    db.commit()
    db.refresh(unit)
    return unit

@app.patch("/api/units/{unit_id}")


@app.delete("/api/units/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.get(UnitDB, unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail=f"Unit {unit_id} not found")
    db.delete(unit)
    db.commit()
    return {"message": f"Unit {unit.callsign} deleted"}