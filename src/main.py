import uvicorn
from fastapi import Depends, FastAPI

from src.auth_dep import verify_api_key
from src.organization.router import router as org_router
from src.utils import get_app_version

app_version = get_app_version()

app = FastAPI(title="TEST API", version=app_version, root_path="/api", dependencies=[Depends(verify_api_key)])

app.include_router(org_router)


@app.get("/")
async def root():
    return {"__version__": app_version, "message": "Привет от бэкенда"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
