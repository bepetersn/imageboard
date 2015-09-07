#!/usr/bin/env python

from flask_script import Manager
from imageboard import app


if __name__ == '__main__':
    manager = Manager(app)
    manager.run(default_command='runserver')

