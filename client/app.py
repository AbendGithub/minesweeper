import requests
import json
import enum


class MinesweeperException(Exception):
    pass


class ActionCell(enum.Enum):
    FLAG = "Flag"
    QUESTION = "Question"
    PRESS = "Press"


class CellState(enum.Enum):
    UNPRESSED = "unpressed"
    CLEARED = "cleared"
    RED_FLAGGED = "red_flagged"
    QUESTIONED = "questioned"
    BOMBED = "bombed"


_HEADERS = {
            "Accept": "application/xml",
            "Content-Type": "application/xml",
        }


class Minesweeper:
    def __init__(self, url):
        self.url = url
        self.game_id = None
        self.rows = None
        self.columns = None
        self.started_at = None
        self.finished_at = None
        self.grid = None
        self.check_connection()

    def check_connection(self):
        response = requests.get(f"{self.url}/is_alive")
        response.raise_for_status()

    def new_game(self, rows=10, columns=10, bombs=40):
        """Create a new game and return its game identifier"""
        if bombs > rows*columns-1:
            raise MinesweeperException("Number of bombs needs to leave at least one cell free")

        data = {"rows": rows,
                "columns": columns,
                "bombs": bombs
                }

        response = requests.post(f"{self.url}/games/", json=data)
        response.raise_for_status()
        json_data = response.json()
        self._load(json_data["data"])

    def get_all_games(self):
        """Fetch all games and return a list with game-id and status pairs"""
        response = requests.get(f"{self.url}/games")
        response.raise_for_status()
        json_data = response.json()

        return json_data["data"]

    def load_game(self):
        """Fetch and load a game"""
        if not self.game_id:
            raise MinesweeperException("Start a new game or load one first")

        response = requests.get(f"{self.url}/games/{self.game_id}")
        response.raise_for_status()
        json_data = response.json()
        self._load(json_data["data"])

    def _load(self, json_game_data):
        """Load attributes with game response"""
        self.game_id = json_game_data["game_id"]
        self.rows = json_game_data["rows"]
        self.columns = json_game_data["columns"]
        self.started_at = json_game_data["started_at"]
        self.finished_at = json_game_data.get("finished_at")
        self._get_grid(json_game_data["grid"])

    def _get_grid(self, json_grid_data):
        """Return a more handy dictionary key-> tuple(x,y) value->tuple(state, bombs)"""
        grid = dict()

        if json_grid_data:
            for cell in json_grid_data:
                grid[(cell["x"], cell["y"])] = (CellState[cell["state"]], cell.get("bombs_around"))

        self.grid = grid

    def do_action_on_cell(self, x, y, action=ActionCell.PRESS):
        """Send an action over a cell"""
        if not self.game_id:
            raise MinesweeperException("Start a new game or load one first")

        if not isinstance(action, ActionCell):
            raise MinesweeperException("Please use an ActionCell enum class object for action")

        if not (x > 0 and y > 0):
            raise MinesweeperException("Please use positive integer values")

        data = {
            "x": x,
            "y": y,
            "action": action.value
        }

        response = requests.put(f"{self.url}/games/{self.game_id}", json=data)
        response.raise_for_status()
        json_data = response.json()

        return json_data


if __name__ == "__main__":
    obj = Minesweeper("http://127.0.0.1:5000")
    obj.new_game()
    print(obj.grid)
