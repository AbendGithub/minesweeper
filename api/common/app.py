from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def app_factory(name, config=None) -> Flask:
    if not config:
        config = {}

    # all apps use the same config and same database
    app = Flask(name)
    app.config.from_object("common.config.base")
    app.config.update(config)

    # initialize database
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        db.create_all()

    return app
