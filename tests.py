#!flask/bin/python
import os
import unittest
from diary import app, db, models, defaults


class TestCase(unittest.TestCase):
  def setUp(self):
    """
    setup database
    """
    app.config["TESTING"] = True
    app.config["CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(defaults.BASEDIR, "db/test.db")
    self.app = app.test_client()
    db.create_all()

    u = models.User("Jelle", "de Jong", "jelle@hoest.nl", "123")
    db.session.add(u)
    db.session.commit()

    d = models.Diary("Mijn dagboek")
    d.owner_id = u.id
    db.session.add(d)
    db.session.commit()

  def tearDown(self):
    """
    remove database
    """
    db.session.remove()
    db.drop_all()
    os.remove(os.path.join(defaults.BASEDIR, "db/test.db"))

  def test_password(self):
    u = models.User.query.get(1)
    assert u.is_password_correct("321") is False
    assert u.is_password_correct("123") is True

  def test_make_unique_slug(self):
    u = models.User.query.get(1)

    d = models.Diary("Mijn dagboek")
    d.owner_id = u.id
    db.session.add(d)
    db.session.commit()

    d1 = models.Diary.query.get(1)
    d2 = models.Diary.query.get(2)
    assert d1.slug == "mijn-dagboek"
    assert d2.slug == "mijn-dagboek-1"
    assert d1.title == d2.title and d1.slug != d2.slug

  def test_redirect(self):
    d = models.Diary.query.get(1)

    rv = self.app.get("/{0}/".format(d.slug))
    assert "Redirecting" in rv.data

  def login(self, emailaddress, password):
    return self.app.post("/login/", data=dict(
      emailaddress=emailaddress,
      password=password
    ), follow_redirects=True)

  def logout(self):
    return self.app.get("/logout/", follow_redirects=True)

  def test_login_logout(self):
    rv = self.login("admin@hoest.nl", "123")
    assert "Inloggegevens niet correct ingevoerd" in rv.data
    rv = self.logout()
    assert "Inloggen" in rv.data
    rv = self.login("jelle@hoest.nl", "123")
    assert "U bent ingelogd" in rv.data


if __name__ == "__main__":
  unittest.main()
