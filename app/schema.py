from pydantic import BaseModel
from enum import Enum

class UnitStatus(str,Enum):
    available = "available"
    en_route = "en_route"
    on_scene = "on_scene"
    unavailable = "unavailable"


class Unit(BaseModel):
    unit_id : int
    callsign : str
    unit_type: str 
    status: str
    location: str

class UnitCreate(BaseModel):
    unit_type: str
    location: str

class UnitStatusUpdate(BaseModel):
    status : UnitStatus
