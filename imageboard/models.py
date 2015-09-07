import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Unicode, Integer, Column, DateTime, ForeignKey, UnicodeText, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.utils import secure_filename
from config import UPLOADS_DIR

db = SQLAlchemy()


class BaseMixin:
    """
    Simple mixin providing some convenience
    methods to all models.

    """

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
    """
    Thread object, which holds some metadata and
    represents a page where a list of posts can be
    found.

    """

    __tablename__ = 'threads'

    def __init__(self, subject=None):
        self.subject = subject

    id = Column(Integer, primary_key=True)
    subject = Column(Unicode(100))


class Post(BaseMixin, db.Model):
    """
    Post object, which represents a single post
    that a poster makes on the forum, encapsulating
    an image, comment, time created, etc.

    """

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
    """
    String serialization of a unique, 32-byte
    IPv4 address in dot-decimal notation, e.g.
    "192.254.0.1".

    Also has a field "blocked" which if set in
    the database, will not let users with this
    IP address create any posts.

    """

    __tablename__ = 'ip_addresses'

    def __init__(self, v4, blocked=None):
        self.v4 = v4
        self.blocked = False if blocked is None else blocked

    id = Column(Integer, primary_key=True)
    v4 = Column(Unicode(15), unique=True)
    blocked = Column(Boolean)


class Poster(BaseMixin, db.Model):
    """
    Poster model, maintaining a unique
    association between an IP address and
    a name.

    In the future, this could be used to
    keep track of what IP addresses make
    use of which names, to store more
    data about posters' devices, or to
    do finer-grained blocking.

    This class also has some APIs for
    creating posts and threads with a
    level of abstraction.

    """

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
    name = Column(Unicode(100), unique=True)
    ip_address_id = Column(ForeignKey('ip_addresses.id'))
    ip_address = relationship('IPAddress',
                              backref=backref('posters', lazy='dynamic'),
                              uselist=False)
