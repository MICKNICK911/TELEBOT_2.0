from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import database_username, database_password, database_hostname, database_port, database_name


SQLALCHEMY_DATABASE_URL = f"postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()
