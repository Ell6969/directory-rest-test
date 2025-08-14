from typing import List

from geoalchemy2 import Geography
from sqlalchemy import CheckConstraint, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column()
    latitude: Mapped[float] = mapped_column(Float(precision=53))
    longitude: Mapped[float] = mapped_column(Float(precision=53))
    geom: Mapped[object] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
    )

    organizations: Mapped[List["Organization"]] = relationship(  # noqa: F821
        back_populates="building", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("latitude >= -90 AND latitude <= 90", name="chk_lat_range"),
        CheckConstraint("longitude >= -180 AND longitude <= 180", name="chk_lon_range"),
        Index("ix_buildings_lat_lon", "latitude", "longitude"),
    )
