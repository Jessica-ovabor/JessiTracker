from flask import Flask
from .routes import cache,limiter
from .extensions import db,login_manager
from .routes import college_tracker

login_manager.login_view = 'college_tracker.login'

def create_app(config_file='settings.py'):
   app=Flask(__name__)
   app.secret_key = 'secretkeys'
   app.config.from_pyfile(config_file)
   db.init_app(app)
   login_manager.init_app(app)
   app.register_blueprint(college_tracker)
   return app
