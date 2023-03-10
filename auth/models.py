import datetime

from fastapi import Depends
from fastapi_users.db import (SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase)
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String, nullable=False)
    registed_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)