from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

web = Flask(__name__)
web.config.from_object(Config)

login = LoginManager(web)
login.login_view = "login"

db = SQLAlchemy(web)
migrate = Migrate(web, db)

from app import routes, models