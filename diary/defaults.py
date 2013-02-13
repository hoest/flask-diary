import os

SECRET_KEY = "<SECRET_KEY>"
DEBUG = True
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

SQLALCHEMY_DATABASE_URI = "sqlite:////{0}/db/diary.db".format(BASEDIR)

CSRF_ENABLED = True

LOCALE = "nl_NL"

UPLOAD_FOLDER = os.path.join(BASEDIR, "uploads")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

THUMBNAIL_WIDTH = 220
THUMBNAIL_HEIGHT = 220
