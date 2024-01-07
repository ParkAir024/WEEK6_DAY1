from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from Config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.users_model import UsersModel
from models import GameModel

from resources.user import bp as user_bp
api.register_blueprint(user_bp)

from resources.games import bp as games_bp
api.register_blueprint(games_bp)