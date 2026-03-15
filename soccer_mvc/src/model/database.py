from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .player import Base

engine = create_engine("sqlite:///players.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)