from fastapi import UploadFile
import shutil


def save_files(path: str, files: list[UploadFile]) -> None:
    for file in files:
        with open(f"{path}/{file.filename}", mode='wb') as buffer:
            shutil.copyfileobj(file.file, buffer)