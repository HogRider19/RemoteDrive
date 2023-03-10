import uvicorn
from fastapi import Depends, FastAPI

from auth.models import User
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.users import auth_backend, get_current_user, fastapi_users
from database.db import create_db_and_tables

from drive.routers import router as drive_router

from config.config import MEDIAPARH

import os


app = FastAPI(title="RemoteDrive")


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    drive_router,
    prefix='/drive',
    tags=['drive'],
)


@app.on_event("startup")
async def on_startup():
    if not os.path.exists(MEDIAPARH):
        os.mkdir(MEDIAPARH)
    await create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info")