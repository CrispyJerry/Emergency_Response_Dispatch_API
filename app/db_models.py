from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class UnitDB(Base):
    __tablename__ = "units"

    unit_id: Mapped[int] = mapped_column(primary_key=True)
    callsign: Mapped[str] = mapped_column(String(20),unique=True)
    unit_type: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(20), default="available")
    station_location: Mapped[str] = mapped_column(String(100))