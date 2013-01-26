from diary import db
from datetime import datetime


ROLE_USER = 0
ROLE_ADMIN = 1

dairy_user_table = db.Table("dairy_user", db.Model.metadata,
  db.Column("diary_id", db.Integer, db.ForeignKey("diary.id")),
  db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class User(db.Model):
  """
  The User object
  """
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(256))
  lastname = db.Column(db.String(256), nullable=False, index=True)
  emailaddress = db.Column(db.String(1024), nullable=False, index=True, unique=True)
  role = db.Column(db.SmallInteger, default=ROLE_USER)
  created = db.Column(db.DateTime, default=datetime.now)

  # relations
  diaries = db.relationship("Diary", secondary=dairy_user_table, backref="users")
  posts = db.relationship("Post", backref="users")


class Diary(db.Model):
  """
  The Diary object
  """
  __tablename__ = "diary"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  created = db.Column(db.DateTime, default=datetime.now)

  # relations
  posts = db.relationship("Post", backref="diaries")


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
  created = db.Column(db.DateTime, default=datetime.now)
  modified = db.Column(db.DateTime, default=datetime.now)

  # relations
  pictures = db.relationship("Picture", backref="posts")


class Picture(db.Model):
  """
  The Picture object
  """
  __tablename__ = "picture"

  id = db.Column(db.Integer, primary_key=True)
  post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
  title = db.Column(db.String(1024), nullable=False, index=True)
  file = db.Column(db.Binary, nullable=False)
