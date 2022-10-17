import os

from flask import Flask
from flask_cors import CORS

from flaskr import db, auth
from flaskr.models import *


def create_app(test_config=None):
	"""
	create_app is the application factory function.

	app = Flask(__name__, instance_relative_config=True) creates the Flask instance.
		__name__ is the name of the current Python module. The app needs to know where it’s located
		to set up some paths.
		instance_relative_config=True tells the app that configuration files are relative to the
		instance folder. The instance folder is located outside the flaskr package and can hold
		local data that should not be committed to version control, such as configuration secrets
		and the database file.

	app.config.from_mapping() sets some default configuration that the app will use:
		SECRET_KEY is used by Flask and extensions to keep data safe. It’s set to 'dev' to provide
		a convenient value during development, but it should be overridden with a random value when
		deploying.
		DATABASE is the path where the SQLite database file will be saved. It’s under
		app.instance_path, which is the path that Flask has chosen for the instance folder.

	app.config.from_pyfile() overrides the default configuration with values taken from the
	config.py file in the instance folder if it exists (NOT). For example, when deploying, this can
	be used to set a real SECRET_KEY.

	test_config can also be passed to the factory, and will be used instead of the instance
	configuration. This is so the tests you’ll write later in the tutorial can be configured
	independently of any development values you have configured.

	os.makedirs() ensures that app.instance_path exists. Flask does not create the instance folder
	automatically, but it needs to be created because your project will create the SQLite database
	file there.
	"""
	app = Flask(__name__, instance_relative_config=True)
	CORS(app, supports_credentials=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)
	app.config['MAIL_SERVER'] = 'smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = 'dev.project.mail.sender@gmail.com'
	app.config['MAIL_DEFAULT_SENDER'] = 'dev.project.mail.sender@gmail.com'
	app.config['MAIL_PASSWORD'] = open(f"{os.path.dirname(os.path.abspath(__file__))}/../../secrets/mail-password").read()
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	app.config['SESSION_COOKIE_SAMESITE'] = "None"
	app.config['SESSION_COOKIE_SECURE'] = True

	if test_config is None:
		# load the instance config if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	db.init_app(app)
	app.register_blueprint(auth.bp)
	app.register_blueprint(user.bp)
	app.register_blueprint(tag.bp)
	return app
