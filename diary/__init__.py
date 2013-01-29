from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from diary import defaults

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

from diary import views, models
