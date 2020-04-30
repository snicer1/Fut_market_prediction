import enum
from typing import Any
from sqlalchemy import Column, Date, Enum, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()
metadata = Base.metadata

class level(enum.Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"

class foot(enum.Enum):
    right = "right"
    left = "left"

class work_rate(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Player(Base):
    __tablename__ = 'Player'
    futbin_id = Column("futbin_id", Integer, primary_key=True)
    name = Column(String, nullable=False)
    player_id = Column(Integer, nullable=False, unique=True)
    position = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    club = Column(String, nullable=False)
    nation = Column(String, nullable=False)
    league = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    level = Column("meal_type", Enum(level), nullable=False)
    skills = Column(Integer, nullable=False)
    weak_foot = Column(Integer, nullable=False)
    revision = Column(String, nullable=False)
    foot = Column("meal_type", Enum(foot), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    def_wr = Column("def_wr", Enum(work_rate), nullable=False)
    att_wr = Column("att_wr", Enum(work_rate), nullable=False)
    added_on = Column(Date, nullable=False)
    metadata.create_all(checkfirst=True)

class Player(Base):
    __tablename__ = 'Player'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    futbin_id = Column(Integer, ForeignKey("Player.futbin_id"))
    pace = Column(Integer, nullable=False)
    pace_acceleration = Column(Integer, nullable=False)
    pace_sprintspeed = Column(Integer, nullable=False)
    dribbling = Column(Integer, nullable=False)
    dribbling_agility = Column(Integer, nullable=False)
    dribbling_balance = Column(Integer, nullable=False)
    dribbling_reactions = Column(Integer, nullable=False)
    dribbling_ballcontrol = Column(Integer, nullable=False)
    dribbling_dribbling = Column(Integer, nullable=False)
    dribbling_composure = Column(Integer, nullable=False)
    shooting = Column(Integer, nullable=False)
    shooting_positioning = Column(Integer, nullable=False)
    shooting_finishing = Column(Integer, nullable=False)
    shooting_shotpower = Column(Integer, nullable=False)
    shooting_longshots = Column(Integer, nullable=False)
    shooting_volleys = Column(Integer, nullable=False)
    shooting_penalties = Column(Integer, nullable=False)
    passing = Column(Integer, nullable=False)
    passing_vision = Column(Integer, nullable=False)
    passing_crossing = Column(Integer, nullable=False)
    passing_fkaccurancy = Column(Integer, nullable=False)
    passing_shortpassing = Column(Integer, nullable=False)
    passing_longpassing = Column(Integer, nullable=False)
    passing_curve = Column(Integer, nullable=False)
    defending = Column(Integer, nullable=False)
    defending_interceptions = Column(Integer, nullable=False)
    defending_headingaccuramcy = Column(Integer, nullable=False)
    defending_defawareness = Column(Integer, nullable=False)
    defending_standingtackle = Column(Integer, nullable=False)
    defending_slidingtackle = Column(Integer, nullable=False)
    physicality = Column(Integer, nullable=False)
    physicality_jumping = Column(Integer, nullable=False)
    physicality_stamina = Column(Integer, nullable=False)
    physicality_strength = Column(Integer, nullable=False)
    physicality_aggression = Column(Integer, nullable=False)
    metadata.create_all(checkfirst=True)

