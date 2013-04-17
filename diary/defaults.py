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

FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""

MAIL_SERVER = "smtp.webfaction.com"
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = "Online Dagboek <noreply@online-daboek.nl>"
MAIL_DEFAULT_BCC = "jelle@hoest.nl"
