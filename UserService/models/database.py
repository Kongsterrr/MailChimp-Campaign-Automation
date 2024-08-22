from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
db = Session()

Base = declarative_base()


def initialize_db():
    Base.metadata.create_all(bind=engine)
