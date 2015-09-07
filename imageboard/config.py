
"""
Settings file.

"""

import os


DEBUG = True
SECRET_KEY = 'fake'
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
