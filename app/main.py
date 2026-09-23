from fastapi import FastAPI, HTTPException
from app.schema import Unit, UnitCreate, UnitStatusUpdate

app = FastAPI()

units = [
    Unit(
        unit_id=1,
        callsign="AMB-1",
        unit_type="Ambulance",
        status="available",
        location="Dublin"
    ),
    Unit(
        unit_id=2,
        callsign="AMB-2",
        unit_type="Ambulance",
        status="on_scene",
        location="Dublin"
    ),
    Unit(
        unit_id=3,
        callsign="FT-1",
        unit_type="Firetruck",
        status="available",
        location="Dublin"
    ),
    Unit(
        unit_id=4,
        callsign="FT-1",
        unit_type="Firetruck",
        status="en_route",
        location="Dublin"
    ),
    Unit(
        unit_id=5,
        callsign="FT-1",
        unit_type="Firetruck",
        status="on_scene",
        location="Dublin"
    )

]


@app.get("/")
def root():
    return {"message": "Unit Management API is running"}

@app.get("/api/units/getall")
def get_all_units():
    return units


@app.get("/api/units/fire")
def get_firetruck():
    firetrucks = []

    for unit in units:
        if unit.unit_type == "Firetruck":
            firetrucks.append(unit)

    return firetrucks

@app.get("/api/units/ambulance")
def get_ambulance():
    ambulances = []

    for unit in units:
        if unit.unit_type == "Ambulance":
            ambulances.append(unit)

    return ambulances


@app.get("/api/units")
def get_units(
    status: str | None = None,
    unit_type: str | None = None
):
    filtered_units = units

    if status is not None:
        filtered_units = []

        for unit in units:
            if unit.status == status:
                filtered_units.append(unit)

    if unit_type is not None:
        filtered_units = [
            unit for unit in filtered_units
            if unit.unit_type == unit_type
        ]

    return filtered_units

@app.post("/api/units")
def create_unit(unit: UnitCreate):
    new_unit_id = len(units) + 1

    if unit.unit_type == "Ambulance":
        abbreviation = "AMB"
    elif unit.unit_type == "Firetruck":
        abbreviation = "FT"
    else:
        abbreviation = "UNIT"

    new_unit = Unit(
        unit_id = new_unit_id,
        callsign=f"{abbreviation}-{new_unit_id}",
        unit_type=unit.unit_type,
        status="available",
        location=unit.location
    )

    units.append(new_unit)

    return new_unit

@app.patch("/api/units/{unit_id}/status")
def update_status(unit_id: int, status_update: UnitStatusUpdate):
    for unit in units:
        if unit.unit_id == unit_id:
            unit.status = status_update.status
            return unit
    raise HTTPException(
            status_code=404,
            detail="Unit not found"
        )

@app.delete("/api/units/{unit_id}")
def delete_unit(unit_id: int):
    for unit in units:
        if unit.unit_id == unit_id:
            units.remove(unit)
            return {"message": "Unit deleted"}

    raise HTTPException(
            status_code=404,
            detail="Unit not found"
        )

@app.get("/api/units/{unit_id}")
def get_unit_id(unit_id: int):
    for unit in units:
        if unit.unit_id == unit_id:
            return unit

    raise HTTPException(
        status_code=404,
        detail="Unit not found"
    )