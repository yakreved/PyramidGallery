import sqlalchemy #начните работу с этой библиотеки
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://user:pass@localhost:5432/postgres')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    comments = relationship("Comment", backref="user")
    isadmin = Column(Boolean)

    def __init__(self, name, password, isadmin):
        self.name = name
        self.password = password
        self.isadmin = isadmin

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.password, self.isadmin)


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    url = Column(String)
    date = Column(DateTime)
    fk_owner = Column(Integer)
    fk_gallery = Column(Integer)

    def __init__(self, name, description, url, date, fk_gallery=None, fk_owner=None):
        self.name = name
        self.description = description
        self.url = url
        self.date = date
        self.fk_gallery = fk_gallery
        self.fk_owner = fk_owner

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.description)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    fk_owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    fk_image = Column(Integer)
    date = Column(DateTime)
    text = Column(String)

    def __init__(self, fk_owner, fk_image, date, text):
        self.fk_owner = fk_owner
        self.fk_image = fk_image
        self.date = date
        self.text = text

    def __repr__(self):
        return "<Comment('%s')>" % self.text


print("Base generating...")
metadata = Base.metadata
metadata.create_all(engine)
print("DONE")