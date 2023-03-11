from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database.db import Base


class Directory(Base):
    __tablename__ = 'directories'

    id: UUID = Column(UUID, primary_key=True, unique=True)
    name: str = Column(String(250), nullable=False)
    is_public: bool = Column(Boolean, nullable=False, default=False)
    
    user_id: UUID = Column(UUID, ForeignKey('users.id'))

    files = relationship('RemoteFile', backref='directory')


class RemoteFile(Base):
    __tablename__ = 'files'

    id: UUID = Column(UUID, primary_key=True, unique=True)
    name: str = Column(String(250), nullable=False)
    create_at: TIMESTAMP = Column(TIMESTAMP, default=datetime.utcnow)
    path: str = Column(String, nullable=False)

    directory_id: UUID = Column(UUID, ForeignKey('directories.id'))

