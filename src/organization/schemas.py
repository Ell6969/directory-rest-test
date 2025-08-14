from datetime import datetime

from pydantic import BaseModel, Field

from src.constant import ModelFieldConst


class SOrgAll(BaseModel):
    id: int | None = None
    name: str = Field("", max_length=ModelFieldConst.ORG_NAME)
    building_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SGeoRadius(BaseModel):
    lat: float | None = None
    lon: float | None = None
    radius_m: float | None = None

    model_config = {"from_attributes": True}


class SGeoBbox(BaseModel):
    bbox: str | None = None

    model_config = {"from_attributes": True}
