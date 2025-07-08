from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class Voter(Base):
    __tablename__ = "voters"

    name = Column(String, primary_key=True, index=True)
    choice1 = Column(Integer)
    choice2 = Column(Integer)
    choice3 = Column(Integer)
    assigned_land = Column(Integer, nullable=True)

class DraftResult(Base):
    __tablename__ = "draft_results"

    round_num = Column(Integer, primary_key=True, index=True)
    results = Column(JSON)
