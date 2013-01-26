from flask import render_template
from diary import app


@app.route('/')
@app.route('/index')
def index():
  return render_template("home.html", basedir=app.config["BASEDIR"])
