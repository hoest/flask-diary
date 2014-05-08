from diary import defaults
from flask import Flask, g
from flask.ext.assets import Environment, Bundle
from flask.ext.login import LoginManager, current_user
from flask_flatpages import FlatPages
from flask_mail import Mail
from flask_oauth import OAuth
from flask_sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from flaskext.markdown import Markdown
from werkzeug import SharedDataMiddleware
import flask.ext.restless
import locale


# create application
app = Flask(__name__)
# app.jinja_env.add_extension("jinja2htmlcompress.HTMLCompress")

# configuration
app.config.from_object(defaults)
app.config.from_envvar("FLASK_DIARY_SETTINGS", silent=True)

# Assets
assets = Environment(app)
js = Bundle("js/bootstrap.min.js",
            "fancybox/jquery.fancybox.pack.js",
            "js/jquery.infinitescroll.min.js",
            "js/diary.js",
            filters="jsmin",
            output="gen/packed.%(version)s.js")

assets.register("js_all", js)

css = Bundle("css/bootstrap.min.css",
             "css/style.css",
             "fancybox/jquery.fancybox.css",
             filters="cssmin",
             output="gen/packed.%(version)s.css")
assets.register("css_all", css)

# Mail
mail = Mail(app)

# Uploads
app.add_url_rule("/uploads/<post_id>/<filename>",
                 "uploaded_file",
                 build_only=True)
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
                            request_token_params={"scope": "email"})

from diary import views, models


def auth_func(*args, **kw):
  if not current_user.is_authenticated():
    raise flask.ext.restless.ProcessingException(description="Not authenticated!", code=401)


def get_single_preprocessor(instance_id=None, **kw):
  """
  Accepts a single argument, `instance_id`, the primary key of the
  instance of the model to get.
  """
  if g.user is not None and current_user.is_authenticated():
    if not g.user.has_access(instance_id):
      raise flask.ext.restless.ProcessingException(description="Not authenticated!", code=401)


def get_many_preprocessor(search_params=None, **kw):
  """
  Accepts a single argument, `search_params`, which is a dictionary
  containing the search parameters for the request.
  """
  if g.user is not None and current_user.is_authenticated():
    filt = dict(name="users",
                op="any",
                val=dict(name="id",
                         op="eq",
                         val=g.user.id))

    # Check if there are any filters there already.
    if "filters" not in search_params:
      search_params["filters"] = []

    # *Append* your filter to the list of filters.
    search_params["filters"].append(filt)


def sort_by_date_preprocessor(search_params=None, **kw):
  if g.user is not None and current_user.is_authenticated():
    order = dict(field="date", direction="desc")

    # Check if there are any order_by there already.
    if "order_by" not in search_params:
      search_params["order_by"] = []

    # *Append* your filter to the list of order_by.
    search_params["order_by"].append(order)


# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app,
                                        preprocessors=dict(GET_SINGLE=[auth_func, get_single_preprocessor],
                                                           GET_MANY=[auth_func, get_many_preprocessor, sort_by_date_preprocessor],
                                                           PUT_SINGLE=[auth_func],
                                                           POST=[auth_func],
                                                           DELETE=[auth_func]),
                                        flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(models.Diary,
                   exclude_columns=["posts", "users"],
                   methods=["GET", "POST", "DELETE", "PUT_SINGLE"])
