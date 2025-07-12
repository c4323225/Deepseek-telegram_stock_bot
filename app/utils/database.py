import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50))
    referral_count = Column(Integer, default=0)
    invited_by = Column(Integer, default=0)  # Storing the user_id of the referrer

class Referral(Base):
    __tablename__ = 'referrals'
    id = Column(Integer, primary_key=True)
    referrer_id = Column(Integer)
    referred_id = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

def init_db():
    engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///stockbot.db"))
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
