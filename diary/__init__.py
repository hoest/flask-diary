from diary import defaults
from flask import Flask
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt

# create application
app = Flask(__name__)

# configuration
app.config.from_object(defaults)
app.config.from_envvar("SETTINGS", silent=True)

# SQLAlchemy
db = SQLAlchemy(app)

# Flask-Login
lm = LoginManager()
lm.setup_app(app)

# Flask Bcrypt (passwords)
bcrypt = Bcrypt(app)

from diary import views, models
