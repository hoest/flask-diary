from datetime import datetime
from diary import app, models, db, forms, lm
from flask import g, session, render_template, redirect, url_for, flash, request
from flask.ext.login import login_required, logout_user, login_user

USER_ID = 1  # test user-id


@app.teardown_request
def teardown_request(exception=None):
  """
  Closes the database again at the end of the request.
  """
  db.session.close()


@app.before_request
def check_user_status():
  """
  Check global user_id
  """
  g.user = None
  if "user_id" in session:
    g.user = models.User.query.get(session["user_id"])


@lm.user_loader
def load_user(user_id):
  """
  LoginManager method
  """
  return models.User.get(user_id)


@app.route("/")
# @login_required
def diary_index():
  """
  Shows all available diaries, includes a form to create a new one.
  """
  diaries = models.Diary.query.filter(models.Diary.user_id == USER_ID)
  return render_template("diary_index.html", diaries=diaries)


@app.route("/create/", methods=["POST", "GET"])
# @login_required
def diary_create():
  """
  Create a new diary for the current user
  """
  form = forms.DiaryForm()

  if form.validate_on_submit():
    diary = models.Diary(request.form["title"])
    diary.user_id = USER_ID

    db.session.add(diary)
    db.session.commit()
    flash("Dagboek toegevoegd")
    return redirect(url_for("diary_index"))
  # else:
  #   flash("Dagboek is niet correct ingevoerd")

  return render_template("diary_create.html", form=form)


@app.route("/<path:diary_slug>/edit/", methods=["POST", "GET"])
# @login_required
def diary_edit(diary_slug):
  """
  Edit diary for the current user
  """
  diary = models.Diary.query.filter(models.Diary.slug == diary_slug).first_or_404()
  form = forms.DiaryForm(obj=diary)

  if form.validate_on_submit():
    form.populate_obj(diary)
    diary.create_slug()

    db.session.add(diary)
    db.session.commit()
    flash("Dagboek gewijzigd")
    return redirect(url_for("diary_index"))
  # else:
  #   flash("Dagboek is niet correct ingevoerd")

  return render_template("diary_create.html", form=form)


@app.route("/delete/<int:diary_id>/")
# @login_required
def diary_delete(diary_id):
  diary = models.Diary.query.get(diary_id)
  db.session.delete(diary)
  db.session.commit()

  flash("Dagboek verwijderd")
  return redirect(url_for("diary_index"))


@app.route("/<path:diary_slug>/")
# @login_required
def post_index(diary_slug):
  """
  Shows all available posts in the current diary, includes a form to add a new
  post to this diary.
  """
  diary = models.Diary.query.filter(models.Diary.slug == diary_slug).first_or_404()
  posts = models.Post.query.filter(models.Post.diary_id == diary.id)

  return render_template("post_index.html", diary=diary, posts=posts)


@app.route("/<path:diary_slug>/create/", methods=["GET", "POST"])
# @login_required
def post_create(diary_slug):
  """
  POST-method to create a new post
  """
  diary = models.Diary.query.filter(models.Diary.slug == diary_slug).first_or_404()

  form = forms.PostForm()

  if form.validate_on_submit():
    post = models.Post(diary.id, request.form["title"])
    post.user_id = USER_ID
    post.diary_id = diary.id

    form.populate_obj(post)

    db.session.add(post)
    db.session.commit()

    flash("Bericht toegevoegd")
    return redirect(url_for("post_index", diary_slug=diary.slug))
  # else:
  #   flash("Bericht is niet correct ingevoerd")

  return render_template("post_create.html", form=form, diary=diary)


@app.route("/<path:diary_slug>/<path:post_slug>/edit/", methods=["GET", "POST"])
# @login_required
def post_edit(diary_slug, post_slug):
  """
  POST-method to edit post
  """
  diary = models.Diary.query.filter(models.Diary.slug == diary_slug).first_or_404()
  post = models.Post.query.filter(models.Post.slug == post_slug, models.Post.diary_id == diary.id).first_or_404()

  form = forms.PostForm(obj=post)

  if form.validate_on_submit():
    form.populate_obj(post)
    post.create_slug(diary.id)
    db.session.add(post)
    db.session.commit()

    flash("Bericht gewijzigd")
    return redirect(url_for("post_index", diary_slug=diary.slug))
  # else:
  #   flash("Bericht is niet correct ingevoerd")

  return render_template("post_create.html", form=form, diary=diary)


@app.route("/<path:diary_slug>/<path:post_slug>/")
# @login_required
def post_view(diary_slug, post_slug):
  """
  Shows all available posts in the current diary, includes a form to add a new
  post to this diary.
  """
  diary = models.Diary.query.filter(models.Diary.slug == diary_slug).first_or_404()
  post = models.Post.query.filter(models.Post.slug == post_slug, models.Post.diary_id == diary.id).first_or_404()

  return render_template("post_view.html", diary=diary, post=post)


@app.route("/<path:diary_slug>/delete/<int:post_id>/")
# @login_required
def post_delete(diary_slug, post_id):
  post = models.Post.query.get(post_id)
  db.session.delete(post)
  db.session.commit()

  flash("Bericht verwijderd")
  return redirect(url_for("post_index", diary_slug=diary_slug))


@app.route("/login/", methods=["GET", "POST"])
def login():
  form = forms.LoginForm()
  if form.validate_on_submit():
    # login and validate the user...
    user = models.User.query.filter(models.User.emailaddress == request.form["emailaddress"])
    login_user(user)
    flash("Ingelogd")
    return redirect(request.args.get("next") or url_for("diary_index"))
  # else:
  #   flash("Inloggegevens niet correct ingevoerd")

  return render_template("login.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
