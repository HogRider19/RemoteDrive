from fastapi import APIRouter, UploadFile, File, Depends, Form
from auth.users import get_current_user
from auth.schemas import UserRead


router = APIRouter()


@router.post('/directory/upload')
def load_directory(
    dir_name: str = Form(...),
    parent_id: int | None = Form(default=None),
    files: list[UploadFile] = File(...),
    user: UserRead = Depends(get_current_user),
):
    return user