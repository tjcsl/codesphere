from sqlalchemy import Column, Integer, String
from project.database import Base

class ShortenedURL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    short = Column(String(20), unique=True)
    longer = Column(String(512))

    def __init__(self, short=None, longer=None):
        self.short = short
        self.longer = longer

    def __repr__(self):
        return '<ShortURL %s=%s>' % (self.short, self.longer)
