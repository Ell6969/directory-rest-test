from typing import Annotated

from fastapi import Depends

from src.database import AsyncSessionDep
from src.organization.services import OrgService


def get_org_service(session: AsyncSessionDep):
    return OrgService(session)


OrgServiceDEP = Annotated[OrgService, Depends(get_org_service)]
