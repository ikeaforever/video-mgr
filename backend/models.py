import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import Column, String, Integer, SMALLINT, DECIMAL, Enum, TEXT, TIMESTAMP,ForeignKey


from sqlalchemy.orm import DeclarativeBase

Base = declarative_base()

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
    

basedir = os.path.abspath(os.path.dirname(__name__))

engine=   create_engine('sqlite:///' + os.path.join(basedir,'db','data.sqlite'), echo=True, future=True)
DBSession = sessionmaker(bind=engine)
