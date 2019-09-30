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

    def __str__(self):
        return self.name


class CellState(enum.Enum):
    UNPRESSED = "unpressed"
    CLEARED = "cleared"
    RED_FLAGGED = "red_flagged"
    QUESTIONED = "questioned"
    BOMBED = "bombed"

    def __str__(self):
        return self.name


class Game(db.Model):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    mines = Column(Integer, nullable=False)
    state = Column(Enum(GameState), default=GameState.NEW, nullable=False)

    grid = relationship("Cell")

    @classmethod
    def list_all(cls):
        return cls.query.all()


class Cell(db.Model):
    __tablename__ = "cell"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    state = Column(Enum(CellState), default=CellState.UNPRESSED, nullable=False)
    has_bomb = Column(Boolean, default=False, nullable=False)
    bombs_around = Column(Integer)

    __table_args__ = (UniqueConstraint("game_id", "x", "y"),)

    @classmethod
    def generate_grid(cls, game):
        for x in range(1, game.rows + 1):
            for y in range(1, game.columns + 1):
                db.session.add(Cell(game_id=game.id, x=x, y=y))
