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
  populate()


@manager.command
def recreate():
  "Recreates database tables (same as issuing 'drop' and then 'create')"
  drop()
  create()


@manager.command
def populate():
  "Populate database with default data"
  user1 = models.User("Jelle", "de Jong", "jelle@hoest.nl", "123")
  user2 = models.User("Suzanne", "Beugelaar", "suzanne@hoest.nl", "123")
  db.session.add(user1)
  db.session.add(user2)

  diary = models.Diary("Mijn dagboek")
  diary.owner_id = user1.id
  diary.users.append(user1)
  diary.users.append(user2)
  db.session.add(diary)

  db.session.commit()


manager.run()
