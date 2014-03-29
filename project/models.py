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

class Bug(Base):
    __tablename__ = 'bugs'
    id = Column(Integer, primary_key=True)
    title = Column(String(512))
    description = Column(String(10000))
    priority = Column(Enum(['LOW','MEDIUM','HIGH','CRITICAL'], name="priority_enum"))
    bug_type = Column(Enum(['BUG','ENHANCEMENT','OTHER'], name="bug_type_enum"))

    def __init__(self, title, description, priority, bug_type):
        self.title = title
        self.description = description
        self.priority = priority
        self.bug_type = bug_type

    def __repr__(self):
        return '<Bug title=%s priority=%s bug_type=%s desc=%s>' % (self.title, self.priority, self.bug_type, self.description)

class Blocker(Base):
    __tablename__ = 'bug_dependancies'
    id = Column(Integer, primary_key=True)
    blocker = Column(Intenger)
    blockee = Column(Integer)

    def __init__(self, blocker, blockee):
        this.blocker = blocker
        this.blockee = blockee
        return '<Blocker %d is blocked by %d>' % (blocker, blockee)
