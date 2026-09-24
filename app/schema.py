from pydantic import BaseModel,ConfigDict
from enum import Enum

class UnitStatus(str,Enum):
    available = "available"
    en_route = "en_route"
    on_scene = "on_scene"
    unavailable = "unavailable"


class Unit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    unit_id : int
    callsign : str
    unit_type: str 
    status: str
    station_location: str

class UnitCreate(BaseModel):
    unit_type: str
    station_location: str

class UnitUpdate(BaseModel):
    unit_type: str | None = None
    station_location: str | None = None

class UnitStatusUpdate(BaseModel):
    status : UnitStatus
