from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from login.config import Config
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from flask_caching import Cache

import redis
from rq import Queue
import time
import json

r=redis.Redis()
q=Queue(connection=r)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
cache = Cache(config={"CACHE_TYPE":"simple"})

mail = Mail()


def create_app(config_class = Config):
    app = Flask(__name__)

    app.config.from_object(Config)
    cache.init_app(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # config = {
    # "DEBUG": True,          # some Flask specific configs
    # "CACHE_TYPE": "memcached", # Flask-Caching related configs
    # "CACHE_DEFAULT_TIMEOUT": 300
    # }
    
    from login.errors.handlers import errors
    from login.users.routes import users
    from login.posts.routes import posts
    from login.main.routes import main
    from login.bankaccounts.routes import bankaccounts
    from login.stocks.routes import stocks
    
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(bankaccounts)
    app.register_blueprint(stocks)
    return app


# STOCK_VALUE = {'data'= []}
# def get_call():
#     r = requests.get("http://localhost:5001/stocks?no_stocks=100").json()
#     STOCK_VALUE = r #json.loads(r.text)
#     return

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=get_call, trigger="interval", seconds=3)
# scheduler.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())