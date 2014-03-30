from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
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

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(512), nullable=False)
    owner = Column(ForeignKey('users.id'), nullable=False)

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

class Bug(Base):
    __tablename__ = 'bugs'
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    description = Column(String(10000), nullable=False)
    priority = Column(Enum('LOW','MEDIUM','HIGH','CRITICAL', name="priority_enum"), nullable = False)
    bug_type = Column(Enum('BUG','ENHANCEMENT','OTHER', name="bug_type_enum"), nullable = False)
    bug_id = Column(Integer, nullable=False)
    project = Column(Integer, ForeignKey('projects.id'), nullable=False)

    __table_args__ = (UniqueConstraint('bug_id', 'project'),)

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
    blocker = Column(Integer, nullable=False)
    blockee = Column(Integer, nullable=False)

    def __init__(self, blocker, blockee):
        self.blocker = blocker
        self.blockee = blockee
        return '<Blocker %d is blocked by %d>' % (blocker, blockee)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False)
    username = Column(String(256), nullable=False)
    github_access_token = Column(String(256), nullable=False)

    def __init__(self, email, username, github_access_token):
        self.email = email
        self.username = username
        self.github_access_token = github_access_token

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    nick = Column(String(50), nullable=False)
    email = Column(String(256), nullable=False)
    content = Column(String(1000))
    repo = Column(String(300), nullable=False)
    code = Column(ForeignKey('code.id'), nullable=True)

#class Code(Base):
#    __tablename__ = 'code'
#    id = Column(Integer, primary_key=True)
#    lines = relationship('codeline')
#
#class CodeLine(Base):
#    __tablename__ = 'codeline'
#    id = Column(Integer, primary_key=True)
#    number = Column(Integer, nullable=False)
#    codeparent = Column(Integer, ForeignKey('code.id'))
