from common.app import app_factory
from flask_restplus import Api, reqparse
from resources.games import ns as ns_game

app = app_factory(__name__)
api = Api(app, title="MineSweeper API")

api.add_namespace(ns_game, "/games")

if __name__ == "__main__":
    app.run(debug=True)
