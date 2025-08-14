from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from src.config import settings


def verify_api_key(key: str = Header(...)) -> str:
    if key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недопустимый API-ключ")
    return key


ApiKeyDep = Annotated[str, Depends(verify_api_key)]
