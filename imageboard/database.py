"""
SQLAlchemy "declarative" style boilerplate
This setup would let you easily swap out Flask for
another web framework, such as Django, if you wanted,
or to access the ORM outside of a web server / WSGI
application context altogether.

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.
    import imageboard.models
    Base.metadata.create_all(bind=engine)