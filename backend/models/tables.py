import os
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import Column, String, Integer, SMALLINT, DECIMAL, Enum, TEXT, TIMESTAMP,ForeignKey


from sqlalchemy.orm import DeclarativeBase


from sqlalchemy.inspection import inspect


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)
    message = Column(String(256))
    status = Column(String(64), unique=True, index=True) # 0: 未开始， 1： 进行中， 2： 已完成
    create_time = Column(TIMESTAMP)

    def __init__(self, name, status):
        self.name = name
        self.status = status
        self.create_time = datetime.datetime.now()


    def _repr_(self):
        return '<Task %r>' % self.name
   
    def serialize(self):
        d = Serializer.serialize(self)
        return d


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)
    
    def _repr_(self):
        return '<Category %r>' % self.name

class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    file_size = Column(Integer)
    play_info_size = Column(Integer)

    def _repr_(self):
        return '<Video %r>' % self.name
    
    def to_dict():
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "file_size": self.file_size,
            "play_info_size": self.play_info_size
        }
    def serialize(self):
        d = Serializer.serialize(self)
        return d
    

basedir = os.path.abspath(os.path.dirname(__name__))

engine=create_engine('sqlite:///' + os.path.join(basedir,'backend','db','data.sqlite'), echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == '__main__':
    print(basedir)
    Base.metadata.create_all(engine)
