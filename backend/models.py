from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class User(BaseModel):
    username: str
    email: str
    password: str

class UserDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
