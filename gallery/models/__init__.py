import sqlalchemy#начните работу с этой библиотеки
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://user:pass@localhost:5432/postgres')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
 
    def __init__(self, name, password):
        self.name = name
        self.password = password
    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.password)

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    url = Column(String)
    date = Column(DateTime)
    fk_owner = Column(Integer)
    fk_gallery = Column(Integer)
 
    def __init__(self, name, description, url, date, fk_gallery = None, fk_owner = None):
        self.name = name
        self.description = description
        self.url = url
        self.date = date
        self.fk_gallery = fk_gallery
        self.fk_owner = fk_owner

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.description)

metadata = Base.metadata
metadata.create_all(engine)