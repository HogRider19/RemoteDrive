import os

from fastapi import (APIRouter, BackgroundTasks, Depends, File, Form,
                     UploadFile, status)
from fastapi.exceptions import HTTPException
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import UserRead
from auth.users import get_current_user
from config.config import MEDIAPARH
from database.db import get_async_session
from drive.models import Directory
from drive.utils import save_files


router = APIRouter()


@router.post('/directory/upload', status_code=status.HTTP_201_CREATED)
async def load_directory(
    tasks: BackgroundTasks,
    dir_name: str = Form(...),
    parent_id: int | None = Form(default=None),
    files: list[UploadFile] = File(default=[]),
    user: UserRead = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    base_path = f"{MEDIAPARH}/{user.id}"
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    if parent_id is None:
        dir_path = f"{base_path}/{dir_name}"
    else:
        parent_result: Result = await db.execute(
            select(Directory).where(Directory.id==parent_id))
        parent: Directory = parent_result.scalars().first()
        if parent is None or parent.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Invalid parent_id")
        dir_path = f"{base_path}/{parent.path}/{dir_name}"

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        tasks.add_task(save_files, dir_path, files)

    dir_ = Directory(
        name=dir_name,
        path=dir_path,
        user_id=user.id,
    )
    db.add(dir_)
    await db.commit()

    return user