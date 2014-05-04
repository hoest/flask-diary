from diary import app, models, db, forms, lm, pages, facebook, mail
from flask import g, session, render_template, redirect, url_for, flash, request, send_from_directory
from flask.ext.login import login_required, logout_user, login_user
from flask_mail import Message
import os


@app.before_request
def check_user_status():
  """
  Check global user_id
  """
  g.user = None
  g.diaries = None
  if "user_id" in session:
    g.user = models.User.query.get(session["user_id"])
    g.diaries = g.user.sorted_diaries()


@lm.user_loader
def load_user(user_id):
  """
  LoginManager method
  """
  return models.User.query.get(user_id)


@app.route("/favicon.ico")
def favicon():
  return send_from_directory(os.path.join(app.root_path, "static"),
                             "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.route("/")
@app.route("/<path:path>/")
@login_required
def catch_all(path=None):
  """
  All other routes
  """
  return render_template("index.html", user=g.user)


@app.route("/login/", methods=["GET", "POST"])
def login():
  return render_template("login.html")


@app.route("/logout/")
@login_required
def logout():
  logout_user()
  return redirect(url_for("login"))


@app.route("/facebook/login/", methods=["GET"])
def login_facebook():
  """
  Calling into authorize will cause the OpenID auth machinery to kick
  in.  When all worked out as expected, the remote application will
  redirect back to the callback URL provided.
  """
  return facebook.authorize(callback=url_for("facebook_authorized",
                                             next=request.args.get('next') or request.referrer or url_for("catch_all"),
                                             _external=True))


@app.route("/facebook/authorized/")
@facebook.authorized_handler
def facebook_authorized(resp):
  """
  Called after authorization.  After this function finished handling,
  the OAuth information is removed from the session again.  When this
  happened, the tokengetter from above is used to retrieve the oauth
  token and secret.

  Because the remote application could have re-authorized the application
  it is necessary to update the values in the database.

  If the application redirected back after denying, the response passed
  to the function will be `None`.  Otherwise a dictionary with the values
  the application submitted.  Note that Twitter itself does not really
  redirect back unless the user clicks on the application name.
  """
  next_url = "/#%s" % request.args.get('next') or request.referrer or url_for("catch_all")
  if resp is None:
    flash("Probeer opnieuw in te loggen")
    return redirect(next_url)

  session["oauth_token"] = (resp["access_token"], "")
  me = facebook.get("/me")

  user = models.User.query.filter(models.User.emailaddress == me.data["email"]).first()

  if user is None:
    # create new user
    user = models.User(me.data["first_name"], me.data["last_name"], me.data["email"])
    db.session.add(user)
    oauth = models.OAuth(user.id, resp["access_token"])
    db.session.add(oauth)
    db.session.commit()
    send_welcome_mail(user)

  else:
    # use this user and register oauth
    oauth = models.OAuth.query.filter(models.OAuth.user_id == user.id, models.OAuth.oauth_type == models.OAUTH_FACEBOOK).first()

    if oauth is None:
      oauth = models.OAuth(user.id, resp["access_token"])
      send_welcome_mail(user)
    else:
      oauth.oauth_token = resp["access_token"]

    db.session.add(oauth)
    db.session.commit()

  login_user(user, True)
  flash("Je bent ingelogd")

  return redirect(next_url)


def send_welcome_mail(user):
  if app.config["DEBUG"] is True:
    return

  """
  Method to send a welcome-mail to a new Facebook-user
  """
  body = """
  Beste %s,

  Welkom bij Online-dagboek (http://www.online-dagboek.nl/). Vanaf heden kun
  je gebruik maken van de diensten van Online-dagboek, met behulp van je
  Facebook-account kun je inloggen op de site en je berichten schrijven
  in je dagboek.

  Veel plezier!

  M.v.g.,
  Jelle de Jong
  """ % (user.firstname)

  msg = Message(subject="Welkom bij Online-dagboek.nl",
                body=body,
                recipients=[user.emailaddress],
                bcc=[app.config["MAIL_DEFAULT_BCC"]])
  mail.send(msg)


@facebook.tokengetter
def get_oauth_token():
  """
  This is used by the API to look for the auth token and secret
  it should use for API calls.  During the authorization handshake
  a temporary set of token and secret is used, but afterwards this
  function has to return the token and secret.  If you don't want
  to store this in the database, consider putting it into the
  session instead.
  """
  return session.get("oauth_token")
