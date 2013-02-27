from flask import url_for, redirect
from flask.ext.wtf import HiddenField, Form, TextField, TextAreaField, \
  PasswordField, Required, FileField, BooleanField
from flask.ext.wtf.html5 import EmailField, DateField
from utils import get_redirect_target, is_safe_url
import datetime


class DiaryForm(Form):
  """
  Form for the Diary object
  """
  title = TextField("Titel", validators=[Required()])


class PostForm(Form):
  """
  Form for the Post object
  """
  title = TextField("Titel", validators=[Required()])
  body = TextAreaField("Tekst", default="Voer hier je tekst in...", validators=[Required()])
  date = DateField("Datum", default=datetime.datetime.now(), validators=[Required()])


class PictureForm(Form):
  """
  Form for the Picture object
  """
  title = TextField("Titel", validators=[Required()])
  file = FileField("Afbeelding", validators=[Required()])


class RedirectForm(Form):
  """
  Form for redirect forms
  """
  next = HiddenField()

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    if not self.next.data:
      self.next.data = get_redirect_target() or ""

  def redirect(self, endpoint="diary_index", **values):
    if is_safe_url(self.next.data):
      return redirect(self.next.data)
    target = get_redirect_target()
    return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
  """
  Form for Login
  """
  emailaddress = EmailField("Emailadres", validators=[Required()])
  password = PasswordField("Wachtwoord", validators=[Required()])
  remember_me = BooleanField("Blijf ingelogd", default=False)
