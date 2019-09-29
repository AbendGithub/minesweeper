from flask_restplus import Resource, Namespace, fields
from models.models import GameState, CellState

ns = Namespace("Game", description="Games related operations")
_new_game = ns.model("New game", {
    "rows": fields.Integer(required=True, description="Number of rows"),
    "columns": fields.Integer(required=True, description="Number of columns"),
    "bombs": fields.Integer(required=True, description="Number of bombs"),
})

_action = ns.model("Action", {
    "x": fields.Integer(required=True, description="Cell row"),
    "y": fields.Integer(required=True, description="Cell column"),
    "action": fields.String(required=True, description="Cell action", enum=["Flag", "Question", "Press"]),
})


_game_status = ns.model("Games status", {
    "game_id": fields.Integer(required=True, description="Game identifier"),
    "status": fields.String(required=True, description="Game status", enum=list(GameState.__members__.keys())),
})


_cell = ns.model("Cell", {
    "row": fields.Integer(required=True, description="Grid row"),
    "column": fields.Integer(required=True, description="Grid column"),
    "state": fields.String(required=True, description="Game status", enum=list(CellState.__members__.keys())),
})

_game = ns.inherit("Game", _game_status, {
    "rows": fields.Integer(required=True, description="Number of rows"),
    "columns": fields.Integer(required=True, description="Number of columns"),
    "bombs": fields.Integer(required=True, description="Number of bombs"),
    "started_at": fields.DateTime(required=True, description="When the game started"),
    "finished_at": fields.DateTime(required=False, description="When the game finished"),
    "Grid": fields.List(fields.Nested(_cell))
})


@ns.route("/")
class GameList(Resource):
    @ns.doc("List of games with its current status")
    @ns.marshal_list_with(_game_status, envelope="data")
    def get(self):
        pass

    @ns.response(201, "Game successfully created.")
    @ns.doc("Create a new game")
    @ns.expect(_new_game, validate=True)
    def post(self):
        pass


@ns.route("/<game_id>")
@ns.param("game_id", "The game identifier")
@ns.response(404, "Game not found.")
class Game(Resource):
    @ns.doc("Get full data of a game")
    @ns.marshal_with(_game, envelope="data")
    def get(self, game_id):
        pass

    @ns.doc("Apply and action on a cell")
    @ns.marshal_with(_game, envelope="data")
    @ns.expect(_action, validate=True)
    def put(self, game_id):
        pass

