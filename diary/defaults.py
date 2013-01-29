import os

SECRET_KEY = "AAP!"
DEBUG = True
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

SQLALCHEMY_DATABASE_URI = "sqlite:////{0}/db/diary.db".format(BASEDIR)

CSRF_ENABLED = True
