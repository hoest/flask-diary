from flask.ext.wtf import Form, TextField, DateField, PasswordField
from flask.ext.wtf.html5 import EmailField


class DiaryForm(Form):
    title = TextField("Titel")


class PostForm(Form):
    title = TextField("Titel")
    body = TextField("Tekst")
    date = DateField("Datum")


class LoginForm(Form):
    emailaddress = EmailField("Emailadres")
    password = PasswordField("Wachtwoord")
