from sqlalchemy.orm import relationship, backref
from werkzeug.utils import cached_property
from database import Base, db_session

from sqlalchemy import Unicode, Integer, Column, DateTime, ForeignKey, UnicodeText
from datetime import datetime


class BaseMixin:

    def save(self):
        db_session.add(self)
        db_session.commit()


class Thread(BaseMixin, Base):

    __tablename__ = 'threads'

    def __init__(self, subject=None):
        self.subject = subject

    @classmethod
    def from_details(cls, subject, name, comment=None):
        thread = cls(subject)
        thread.save()
        p = Post(name, comment, thread)
        p.save()
        return thread

    @cached_property
    def details(self):
        return self.posts.first()

    id = Column(Integer, primary_key=True)
    subject = Column(Unicode)


class Post(BaseMixin, Base):

    __tablename__ = 'posts'

    def __init__(self, name=None, comment=None, thread=None):
        self.name = name
        self.comment = comment
        self.thread = thread
        self.time_created = datetime.utcnow()

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    comment = Column(UnicodeText)
    time_created = Column(DateTime)
    thread_id = Column(ForeignKey('threads.id'))
    thread = relationship('Thread',
                            backref=backref('posts', lazy='dynamic'),
                            uselist=False)