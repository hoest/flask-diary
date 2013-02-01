from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField, Required
from flask.ext.wtf.html5 import EmailField, DateField


class DiaryForm(Form):
    title = TextField("Titel", validators=[Required()])


class PostForm(Form):
    title = TextField("Titel", validators=[Required()])
    body = TextAreaField("Tekst", validators=[Required()])
    date = DateField("Datum", validators=[Required()])


class LoginForm(Form):
    emailaddress = EmailField("Emailadres", validators=[Required()])
    password = PasswordField("Wachtwoord", validators=[Required()])
