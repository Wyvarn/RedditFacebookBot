"""
Models in application

So the user table has two fields. The name will be the id sent with the Facebook Messenger Webhook request. 
The posts will be linked to the other table, "Posts". 
The Posts table has name and url field. "name" will be populated by the reddit submission id 
and the url will be populated by the url of that post. 
"""

from app import db
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Boolean, Table,\
    PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref, dynamic
from abc import ABCMeta, abstractmethod
from hashlib import md5
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

relationship_table = Table('relationship_table',
                           Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
                           Column('post_id', Integer, ForeignKey('posts.id'), nullable=False),
                           PrimaryKeyConstraint('user_id', 'post_id'))


class Base(db.Model):
    """
    Base class where all tables inherit from
    """
    __metaclass__ = ABCMeta
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    @abstractmethod
    def __repr__(self):
        """
        :return: representation of this object as a Human readable string
        """
        pass


class Users(Base):
    """
    User table
    """
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    posts = relationship('Posts', secondary=relationship_table, backref='users')

    def __init__(self, name):
        self.name = name


class Posts(Base):
    """
    Posts sent to users
    """
    __tablename__ = "posts"

    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)

    def __init__(self, name, url):
        self.name = name
        self.url = url