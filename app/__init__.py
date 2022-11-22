from flask import Flask
from config import Config

web = Flask(__name__)
web.config.from_object(Config)

from app import routes