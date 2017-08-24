import config
from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.login import LoginManager
from flask_flatpages import FlatPages
from flask_mail import Mail
from flask_oauth import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flaskext.markdown import Markdown
from werkzeug import SharedDataMiddleware
import locale


# create application
app = Flask(__name__)
# app.jinja_env.add_extension("jinja2htmlcompress.HTMLCompress")

# configuration
app.config.from_object(config)

# Assets
assets = Environment(app)
js = Bundle("js/bootstrap.min.js", "fancybox/jquery.fancybox.pack.js",
            "js/jquery.infinitescroll.min.js", "js/diary.js",
            filters="jsmin", output="gen/packed.%(version)s.js")
assets.register("js_all", js)

css = Bundle("css/bootstrap.min.css", "css/style.css",
             "fancybox/jquery.fancybox.css",
             filters="cssmin", output="gen/packed.%(version)s.css")
assets.register("css_all", css)

# Mail
mail = Mail(app)

# Uploads
app.add_url_rule("/uploads/<post_id>/<filename>", "uploaded_file", build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {"/uploads": app.config["UPLOAD_FOLDER"]})

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
                    extensions=["nl2br", "sane_lists"],
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

# Logging
if not app.debug:
  import logging
  import os.path
  from logging.handlers import RotatingFileHandler
  formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
  log_path = os.path.join(app.config["BASEDIR"], "logs")
  file_handler = RotatingFileHandler(log_path + "/onlinedagboek.log", maxBytes=10000, backupCount=10)
  file_handler.setLevel(logging.WARNING)
  file_handler.setFormatter(formatter)
  app.logger.addHandler(file_handler)


from diary import views, models
