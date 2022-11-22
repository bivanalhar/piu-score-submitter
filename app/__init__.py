from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

web = Flask(__name__)
web.config.from_object(Config)

db = SQLAlchemy(web)
migrate = Migrate(web, db)

from app import routes, models