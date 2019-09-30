from common.app import app_factory
from flask_restplus import Api
from resources.games import ns as ns_game

app = app_factory(__name__)
api = Api(app, title="MineSweeper API")

api.add_namespace(ns_game, "/games")


@app.route("/is_alive")
def ping():
    return "Service is up.", 200


if __name__ == "__main__":
    app.run(debug=True)
