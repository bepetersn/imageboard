from database import Base

from sqlalchemy import Unicode, Integer, Column, DateTime, ForeignKey
from datetime import datetime


class Thread(Base):

    __tablename__ = 'threads'

    def __init__(self, subject, post_id):
        self.subject = subject
        self.time_created = datetime.utcnow()

    def from_details(self, subject, name, comment):
        pass

    id = Column(Integer, primary_key=True)
    subject = Column(Unicode)
    time_created = Column(DateTime)

    