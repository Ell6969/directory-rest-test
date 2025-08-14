from typing import List, Union

from pydantic import BaseModel

from src.organization.schemas import SOrgAll


class SRouterResultList(BaseModel):
    results: List[Union[SOrgAll,]] = []

    model_config = {"from_attributes": True}


class SRouterResult(BaseModel):
    result: SOrgAll | None = None

    model_config = {"from_attributes": True}
