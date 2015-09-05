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

    def __init__(self, subject=None, post_id=None):
        self.subject = subject
        self.post_id = post_id

    @classmethod
    def from_details(cls, subject, name, comment=None):
        p = Post(name, comment)
        p.save()
        t = cls(subject=subject, post_id=p.id)
        t.save()
        return t

    @cached_property
    def time_created(self):
        return Post.query.get(self.post_id).time_created

    id = Column(Integer, primary_key=True)
    subject = Column(Unicode)
    post_id = Column(ForeignKey('posts.id'))


class Post(BaseMixin, Base):

    __tablename__ = 'posts'

    def __init__(self, name=None, comment=None):
        self.name = name
        self.comment = comment
        self.time_created = datetime.utcnow()

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    comment = Column(UnicodeText)
    time_created = Column(DateTime)