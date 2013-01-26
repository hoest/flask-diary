from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from diary import defaults
# from app import models

# create application
app = Flask(__name__)

# configuration
app.config.from_object(defaults)
app.config.from_envvar("SETTINGS", silent=True)

db = SQLAlchemy(app)

from diary import views, models
