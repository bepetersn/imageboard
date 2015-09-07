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

    @classmethod
    def get_or_create(cls, **kwargs):
        inst = cls.query.filter_by(**kwargs).first()
        if inst is None:
            inst = cls(**kwargs)
            inst.save()
        return inst


class Thread(BaseMixin, db.Model):

    __tablename__ = 'threads'

    def __init__(self, subject=None):
        self.subject = subject

    id = Column(Integer, primary_key=True)
    subject = Column(Unicode(100))


class Post(BaseMixin, db.Model):

    __tablename__ = 'posts'

    def __init__(self, image=None, comment=None, thread=None, poster=None):

        if image:
            self.image_path = secure_filename(image.filename)
            image.save(os.path.join(UPLOADS_DIR, self.image_path))

        self.comment = comment
        self.thread = thread
        self.poster = poster
        self.time_created = datetime.utcnow()

    id = Column(Integer, primary_key=True)
    comment = Column(UnicodeText(1500))
    image_path = Column(Unicode(200))
    time_created = Column(DateTime)
    thread_id = Column(ForeignKey('threads.id'))
    thread = relationship('Thread',
                            backref=backref('posts', lazy='dynamic'),
                            uselist=False)
    poster_id = Column(ForeignKey('posters.id'))
    poster = relationship('Poster',
                            backref=backref('posts', lazy='dynamic'),
                            uselist=False)


class IPAddress(BaseMixin, db.Model):

    __tablename__ = 'ip_addresses'

    def __init__(self, v4):

        self.v4 = v4

    id = Column(Integer, primary_key=True)
    v4 = Column(Unicode(15))


class Poster(BaseMixin, db.Model):

    __tablename__ = 'posters'

    def __init__(self, name, ip_address):
        self.name = name
        self.ip_address = ip_address

    def create_thread(self, subject, image, comment=None):
        thread = Thread(subject)
        thread.save()
        p = Post(image=image,
                 comment=comment,
                 thread=thread,
                 poster=self)
        p.save()
        return thread

    def create_post(self, thread, image=None, comment=None):
        p = Post(image=image,
             comment=comment,
             thread=thread,
             poster=self)
        p.save()
        return p

    def __repr__(self):
        return self.name

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    ip_address_id = Column(ForeignKey('ip_addresses.id'))
    ip_address = relationship('IPAddress',
                              backref=backref('posters', lazy='dynamic'),
                              uselist=False)
