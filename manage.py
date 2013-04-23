#!/usr/bin/env python
from flask.ext.script import Manager, Shell, Server, prompt_bool
from diary import app, db, models

manager = Manager(app)

manager.add_command("runserver", Server())
manager.add_command("shell", Shell())


@manager.command
def drop():
  "Drops database tables"
  if prompt_bool("Are you sure you want to lose all your data"):
    db.drop_all()


@manager.command
def create():
  "Creates database tables from sqlalchemy models"
  db.create_all()


@manager.command
def recreate():
  "Recreates database tables (same as issuing 'drop' and then 'create')"
  drop()
  create()
  populate()


@manager.command
def populate():
  "Populate database with default data"
  user1 = models.User("Jelle", "de Jong", "jelle@hoest.nl", "123")
  user2 = models.User("Suzanne", "Beugelaar", "suzanne@hoest.nl", "123")
  db.session.add(user1)
  db.session.add(user2)

  db.session.commit()

  diary = models.Diary("Mijn dagboek")
  diary.owner_id = user1.id
  diary.users.append(user1)
  diary.users.append(user2)
  db.session.add(diary)

  db.session.commit()

  for i in range(1, 25, 1):
    post = models.Post(diary.id, "Bericht %s" % i)
    post.user_id = user1.id
    post.body = "Bericht %s" % i
    db.session.add(post)

  db.session.commit()

manager.run()
