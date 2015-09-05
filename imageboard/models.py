import os
from datetime import datetime
from sqlalchemy import Unicode, Integer, Column, DateTime, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship, backref
from settings import UPLOADS_DIR
from database import Base, db_session


class BaseMixin:

    def save(self):
        db_session.add(self)
        db_session.commit()


class Thread(BaseMixin, Base):

    __tablename__ = 'threads'

    def __init__(self, subject=None):
        self.subject = subject

    @classmethod
    def from_details(cls, subject, name, image, comment=None):
        thread = cls(subject)
        thread.save()
        p = Post(name=name,
                 image=image,
                 comment=comment,
                 thread=thread)
        p.save()
        return thread

    id = Column(Integer, primary_key=True)
    subject = Column(Unicode(100))


class Post(BaseMixin, Base):

    __tablename__ = 'posts'

    def __init__(self, name=None, image=None, comment=None, thread=None):

        self.image_path = image.filename
        image.save(os.path.join(UPLOADS_DIR, image.filename))

        self.name = name
        self.comment = comment
        self.thread = thread
        self.time_created = datetime.utcnow()

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    comment = Column(UnicodeText(1500))
    image_path = Column(Unicode(200))
    time_created = Column(DateTime)
    thread_id = Column(ForeignKey('threads.id'))
    thread = relationship('Thread',
                            backref=backref('posts', lazy='dynamic'),
                            uselist=False)