import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Unicode, Integer, Column, DateTime, ForeignKey, UnicodeText
from sqlalchemy.orm import relationship, backref
from werkzeug.utils import secure_filename
from config import UPLOADS_DIR

db = SQLAlchemy()


class BaseMixin:

    def save(self):
        db.session.add(self)
        db.session.commit()


class Thread(BaseMixin, db.Model):

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


class Post(BaseMixin, db.Model):

    __tablename__ = 'posts'

    def __init__(self, name=None, image=None, comment=None, thread=None):

        if image:
            self.image_path = secure_filename(image.filename)
            image.save(os.path.join(UPLOADS_DIR, self.image_path))

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