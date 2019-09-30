import environ

env = environ.Env()

SQLALCHEMY_DATABASE_URI = env("SQLALCHEMY_DATABASE_URI", default="sqlite:///:memory:")
SQLALCHEMY_TRACK_MODIFICATIONS = env.bool("SQLALCHEMY_TRACK_MODIFICATIONS", default=False)
