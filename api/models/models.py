from common.app import db
import datetime
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Enum,
    Boolean,
    UniqueConstraint,
    ForeignKey,
)


class GameState(enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class CellState(enum.Enum):
    UNPRESSED = "unpressed"
    CLEARED = "cleared"
    RED_FLAGGED = "red_flagged"
    QUESTIONED = "questioned"
    BOMBED = "bombed"


class Game(db.Model):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    mines = Column(Integer, nullable=False)
    state = Column(Enum(GameState), default=GameState.NEW, nullable=False)

    cells = relationship("Cell")


class Cell(db.Model):
    __tablename__ = "cell"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    state = Column(Enum(CellState), default=CellState.UNPRESSED, nullable=False)
    has_bomb = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint("game_id", "x", "y"),)
