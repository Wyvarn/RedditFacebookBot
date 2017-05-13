"""
Models in application

So the user table has two fields. The name will be the id sent with the Facebook Messenger Webhook request. 
The posts will be linked to the other table, "Posts". 
The Posts table has name and url field. "name" will be populated by the reddit submission id 
and the url will be populated by the url of that post. 
"""

from . import db
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey, Table, \
    PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from abc import ABCMeta, abstractmethod

relationship_table = Table('relationship_table',
                           db.metadata,
                           Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
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


class User(Base):
    """
    User table
    """

    __tablename__ = "user"

    name = Column(String(255), nullable=False)
    posts = relationship('Posts', secondary=relationship_table, backref='users')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "id: {}, name:{}, Dates: [Created: {}, Modified: {}]".format(
            self.id, self.name, self.date_created, self.date_modified, self.posts)


class Posts(Base):
    """
    Posts sent to users
    """

    __tablename__ = "posts"

    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url

    def __repr__(self):
        return "Id: {}, Name:{}, url:{}, Dates: [Created: {}, Modified: {}]".format(
            self.id, self.name, self.url, self.date_created, self.date_modified
        )
