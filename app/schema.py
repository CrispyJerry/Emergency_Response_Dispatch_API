from pydantic import BaseModel,ConfigDict, Field
from typing import Literal
from enum import Enum


UnitType = Literal["Ambulance","Firetruck","Police"]
UnitStatus = Literal["available","en_route","arrived"]
ALLOWED_TRANSITIONS = {
    "available" : ["en_route"],
    "en_route" : ["arrived"],
    "arrived" : ["available"],
}

class Unit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    unit_id : int
    callsign : str
    unit_type: str | None = None
    status: UnitStatus | None = None
    station_location: str

class UnitCreate(BaseModel):
    unit_type: UnitType
    station_location: str = Field(min_length=1)

class UnitUpdate(BaseModel):
    unit_type: UnitType | None = None
    station_location: str | None = Field(default=None, min_length=1)

class UnitStatusUpdate(BaseModel):
    status : UnitStatus
