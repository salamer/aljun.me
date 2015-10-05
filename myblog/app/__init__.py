from flask import Flask,render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from flask.ext.login import LoginManager
#from flask.ext.markdown import Markdown
from flask.ext.misaka import Misaka

from config import Config

db=SQLAlchemy()
pagedown=PageDown()
#markdown=Markdown
md=Misaka()

login_manager=LoginManager()

def create_app(config_name):
	app=Flask(__name__)
	app.config.from_object(Config)
	Config.init_app(app)
#	Markdown(app)

	md.init_app(app)
	db.init_app(app)
	pagedown.init_app(app)
	login_manager.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app
