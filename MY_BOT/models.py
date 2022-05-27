from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean


class Memory(Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True, nullable=False)
    listen = Column(String, nullable=False)
    reply = Column(String, nullable=False)
    Author = Column(String, nullable=False)
    published = Column(Boolean, server_default='FALSE', nullable=False)
    created = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


class Users(Base):
    __tablename__ = "users"
    chat_id = Column(String, nullable=False, unique=True, primary_key=True)
    trust = Column(Integer, nullable=False)
    created = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
