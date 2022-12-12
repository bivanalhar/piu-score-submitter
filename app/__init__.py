from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

import logging, os
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler

web = Flask(__name__)
web.config.from_object(Config)

login = LoginManager(web)
login.login_view = "login"

db = SQLAlchemy(web)
migrate = Migrate(web, db, render_as_batch=True)

bootstrap = Bootstrap(web)

from app import routes, models, errors

if not web.debug:
    if web.config['MAIL_SERVER']:
        auth = None
        if web.config['MAIL_USERNAME'] or web.config['MAIL_PASSWORD']:
            auth = (web.config['MAIL_USERNAME'], web.config['MAIL_PASSWORD'])
        secure = None
        if web.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(web.config['MAIL_SERVER'], web.config['MAIL_PORT']),
            fromaddr='no-reply@' + web.config['MAIL_SERVER'],
            toaddrs=web.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        web.logger.addHandler(mail_handler)
    
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/piu_blog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    web.logger.addHandler(file_handler)

    web.logger.setLevel(logging.INFO)
    web.logger.info('PIU blog startup')