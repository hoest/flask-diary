from datetime import datetime
from diary import app, models, db, forms, lm
from flask import render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, logout_user, login_user


USER_ID = 1  # test user-id


@app.teardown_request
def teardown_request(exception=None):
  """
  Closes the database again at the end of the request.
  """
  db.session.close()


@lm.user_loader
def load_user(user_id):
  return models.User.get(user_id)


@app.route("/")
@app.route("/diaries/")
# @login_required
def diary_index():
  """
  Shows all available diaries, includes a form to create a new one.
  """
  diaries = models.Diary.query.filter(models.Diary.user_id == USER_ID)
  form = forms.DiaryForm()

  return render_template("diary_index.html", diaries=diaries, form=form)


@app.route("/diaries/create/", methods=["POST"])
# @login_required
def diary_create():
  """
  POST-method to create a new diary for the current user
  """
  diary = models.Diary()
  diary.user_id = USER_ID
  diary.title = request.form["title"]

  db.session.add(diary)
  db.session.commit()

  flash("Dagboek toegevoegd")

  return redirect(url_for("diary_index"))


@app.route("/diaries/<int:diary_id>/")
@app.route("/diaries/<int:diary_id>/posts/")
# @login_required
def post_index(diary_id):
  """
  Shows all available posts in the current diary, includes a form to add a new
  post to this diary.
  """
  diary = models.Diary.query.get(diary_id)
  posts = models.Post.query.filter(models.Post.diary_id == diary_id)
  form = forms.PostForm()

  return render_template("post_index.html", diary=diary, posts=posts, form=form)


@app.route("/diaries/<int:diary_id>/posts/create/", methods=["POST"])
# @login_required
def post_create(diary_id):
  """
  POST-method to create a new post
  """
  post = models.Post()
  post.user_id = USER_ID
  post.diary_id = diary_id
  post.title = request.form["title"]
  post.body = request.form["body"]
  post.date = datetime.strptime(request.form["date"], "%Y-%m-%d")

  db.session.add(post)
  db.session.commit()

  flash("Bericht toegevoegd")

  return redirect(url_for("post_index", diary_id=diary_id))


@app.route("/login/", methods=["GET", "POST"])
def login():
  form = forms.LoginForm()
  if form.validate_on_submit():
    # login and validate the user...
    user = models.User.query.filter(models.User.emailaddress == request.form["emailaddress"])
    login_user(user)
    flash("Ingelogd")
    return redirect(request.args.get("next") or url_for("diary_index"))
  return render_template("login.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
