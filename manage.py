#!/usr/bin/env python

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from imageboard import app, db


if __name__ == '__main__':
    manager = Manager(app)
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)
    manager.run(default_command='runserver')

