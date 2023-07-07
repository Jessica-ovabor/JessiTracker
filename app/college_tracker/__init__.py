from flask import Flask
# from .routes import cache,limiter
from .extensions import db,login_manager
from .model import User
from .routes import tracker
from flask_migrate import Migrate


login_manager.login_view = 'tracker.login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
def create_app(config_file='settings.py'):
   app=Flask(__name__)
   app.secret_key = 'secretkeys'
   app.config.from_pyfile(config_file)
   db.init_app(app)
   migrate=Migrate(app,db)
   login_manager.init_app(app)
   app.register_blueprint(tracker)
   return app
