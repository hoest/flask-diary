from diary import defaults
from flask import Flask
from flask.ext.login import LoginManager
from flask_flatpages import FlatPages
from flask_oauth import OAuth
from flask_sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from flaskext.markdown import Markdown
from werkzeug import SharedDataMiddleware
import locale


# create application
app = Flask(__name__)

# configuration
app.config.from_object(defaults)
app.config.from_envvar("FLASK_DIARY_SETTINGS", silent=True)

# Uploads
app.add_url_rule("/uploads/<post_id>/<filename>", "uploaded_file", build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  "/uploads": app.config["UPLOAD_FOLDER"]
})

locale.setlocale(locale.LC_ALL, app.config["LOCALE"])

# SQLAlchemy
db = SQLAlchemy(app)

# Flask-Login
lm = LoginManager()
lm.setup_app(app)
lm.login_view = "login"
lm.login_message = u"Je dient in te loggen voor deze site."

# Flask Bcrypt (passwords)
bcrypt = Bcrypt(app)

# Flask Markdown
markdown = Markdown(app,
                    safe_mode=True,
                    output_format="html5",)

# Flask FlatPages
pages = FlatPages(app)

# Flask OAuth
oauth = OAuth()

# Facebook
facebook = oauth.remote_app("facebook",
  base_url="https://graph.facebook.com/",
  request_token_url=None,
  access_token_url="/oauth/access_token",
  authorize_url="https://www.facebook.com/dialog/oauth",
  consumer_key=app.config["FACEBOOK_APP_ID"],
  consumer_secret=app.config["FACEBOOK_APP_SECRET"],
  request_token_params={"scope": "email"}
)

from diary import views, models
