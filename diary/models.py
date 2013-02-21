from diary import db, utils, bcrypt
from datetime import datetime
from flask.ext.login import UserMixin


ROLE_USER = 0
ROLE_ADMIN = 1

dairy_user_table = db.Table(
  "dairy_user",
  db.Model.metadata,
  db.Column("diary_id", db.Integer, db.ForeignKey("diary.id")),
  db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class User(db.Model, UserMixin):
  """
  The User object
  """
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(256), nullable=False)
  lastname = db.Column(db.String(256), nullable=False, index=True)
  emailaddress = db.Column(db.String(1024), nullable=False, index=True, unique=True)
  password = db.Column(db.String(1024), nullable=False)
  role = db.Column(db.SmallInteger, default=ROLE_USER)
  active = db.Column(db.Boolean, default=True)
  created = db.Column(db.DateTime, default=datetime.now)

  # relations
  diaries = db.relationship("Diary", secondary=dairy_user_table, lazy="dynamic", backref="users")
  posts = db.relationship("Post", lazy="dynamic")

  def __init__(self, firstname, lastname, emailaddress, password):
    self.firstname = firstname
    self.lastname = lastname
    self.emailaddress = emailaddress
    self.password = bcrypt.generate_password_hash(password)

  def is_password_correct(self, password):
    return bcrypt.check_password_hash(self.password, password)

  def get_diary(self, slug):
    return self.diaries.filter(Diary.slug == slug)

  def sorted_diaries(self):
    return self.diaries.order_by(Diary.title)

  def __repr__(self):
    return u"<User %s>" % (self.emailaddress)


class Diary(db.Model):
  """
  The Diary object
  """
  __tablename__ = "diary"

  id = db.Column(db.Integer, primary_key=True)
  owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  slug = db.Column(db.String(256), nullable=False, unique=True)
  created = db.Column(db.DateTime, default=datetime.now)

  # relations
  posts = db.relationship("Post", lazy="dynamic")

  def __init__(self, title):
    self.title = title
    self.create_slug()

  def create_slug(self):
    self.slug = utils.slugify(self.title)

    counter = 0
    new = self.slug
    while self.query.filter(Diary.slug == new).first() is not None:
      counter += 1
      new = "{0}-{1}".format(self.slug, counter)
    self.slug = new

  def get_post(self, slug):
    return self.posts.filter(Post.slug == slug)

  def sorted_posts(self):
    return self.posts.order_by(Post.date.desc())

  def __repr__(self):
    return u"<Diary %s>" % (self.title)


class Post(db.Model):
  """
  The Post object
  """
  __tablename__ = "post"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  diary_id = db.Column(db.Integer, db.ForeignKey("diary.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  body = db.Column(db.Text, nullable=False)
  date = db.Column(db.Date, default=datetime.now)
  slug = db.Column(db.String(256), nullable=False)
  created = db.Column(db.DateTime, default=datetime.now)
  modified = db.Column(db.DateTime, default=datetime.now)

  # relations
  pictures = db.relationship("Picture", lazy="dynamic")

  def __init__(self, diary_id, title):
    self.title = title
    self.create_slug(diary_id)

  def create_slug(self, diary_id):
    self.slug = utils.slugify(self.title)

    counter = 0
    new = self.slug
    while self.query.filter(Post.slug == new, Post.diary_id == diary_id).first() is not None:
      counter += 1
      new = "{0}-{1}".format(self.slug, counter)
    self.slug = new

  def __repr__(self):
    return u"<Post %s>" % (self.title)


class Picture(db.Model):
  """
  The Picture object
  """
  __tablename__ = "picture"

  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  file_url = db.Column(db.String(1024), nullable=False)
  thumb_url = db.Column(db.String(1024), nullable=True)
  slug = db.Column(db.String(256), nullable=False)

  def __init__(self, title):
    self.title = title
    self.slug = utils.slugify(title)

  def __repr__(self):
    return u"<Picture %s>" % (self.title)
