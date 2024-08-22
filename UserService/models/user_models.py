from .database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'User'

    userId = Column(Integer, primary_key=True)
    firstName = Column(String(80), nullable=False)
    lastName = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)