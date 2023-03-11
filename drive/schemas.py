from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Directory(BaseModel):
    id: UUID
    name: str
    is_public: bool
    user_id: UUID


class RemoteFile(BaseModel):
    id: UUID
    name: str
    create_at: datetime
    path: str
    directory_id: UUID