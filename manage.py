#!/usr/bin/env python

from flask_script import Manager
from imageboard import app


manager = Manager(app)


@manager.command
def init():
    """
    Create database tables.
    """
    from imageboard import db
    db.create_all()


if __name__ == '__main__':
    manager.run(default_command='runserver')

