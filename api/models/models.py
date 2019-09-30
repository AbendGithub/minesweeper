from common.app import db
import datetime
import enum
import random
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Enum,
    Boolean,
    UniqueConstraint,
    ForeignKey,
    and_,
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
        # creates all rows for the grid
        for x in range(game.rows):
            for y in range(game.columns):
                db.session.add(Cell(game_id=game.id, x=x, y=y))

        db.session.flush()

        # add bombs across the grid
        total_cells = game.rows * game.columns
        for _ in range(game.mines):
            while True:
                cell_number = random.randint(0, total_cells - 1)
                x = cell_number % game.rows
                y = int(cell_number / game.rows)
                cell = Cell.query.filter_by(game_id=game.id, x=x, y=y).one()
                if not cell.has_bomb:
                    cell.has_bomb = True
                    db.session.add(cell)
                    break

        db.session.flush()

        # associate each non-mine cell with number of surrounding mines
        for x in range(game.rows):
            for y in range(game.columns):
                cell = Cell.query.filter_by(game_id=game.id, x=x, y=y, has_bomb=False).one_or_none()
                if cell:
                    cell.bombs_around = Cell.count_surrounding_bombs(game, x, y)
                    db.session.add(cell)

    @classmethod
    def count_surrounding_bombs(cls, game, x, y):
        return cls.query.filter(and_(
            cls.game_id == game.id, (x - 1) <= cls.x, cls.x <= (x + 1), (y - 1) <= cls.y, cls.y <= (y + 1),
            cls.has_bomb)).count()
