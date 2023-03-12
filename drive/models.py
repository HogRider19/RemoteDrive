from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from database.db import Base

from auth.models import User


class Directory(Base):
    __tablename__ = 'directories'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(250), nullable=False)
    is_public: bool = Column(Boolean, nullable=False, default=False)
    path: str = Column(String, nullable=False)
    user_id: int = Column(Integer, ForeignKey(User.id))

    files = relationship('RemoteFile', back_populates='directory')


class RemoteFile(Base):
    __tablename__ = 'files'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(250), nullable=False)
    create_at: TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow)
    directory_id: int = Column(Integer, ForeignKey(Directory.id))

    directory = relationship('Directory', back_populates='files')

