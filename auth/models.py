import datetime

from fastapi import Depends
from fastapi_users.db import (SQLAlchemyBaseUserTableUUID,
                              SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable)
from sqlalchemy import TIMESTAMP, Boolean, Column, String, UUID, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Base, get_async_session


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String(50), unique=True, nullable=False)
    email: str = Column(String(100), nullable=False)
    hashed_password: str = Column(String, nullable=False)
    registed_at: TIMESTAMP = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)

    # directories = relationship('directories', backref='user')


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)