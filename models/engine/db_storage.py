#!/usr/bin/python3
"""
DB Storage for models
"""

import sqlalchemy
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.answer import Answer
from models.attempt import Attempt
from models.category import Category
from models.comment import Comment
from models.post import Post
from models.question import Question
from models.quiz import Quiz
from models.resource import Resource
from models.thread import Thread
from models.user import User

classes = {
    'Answer': Answer,
    'Attempt': Attempt,
    'Category': Category,
    'Comment': Comment,
    'Post': Post,
    'Question': Question,
    'Quiz': Quiz,
    'Resource': Resource,
    'Thread': Thread,
    'User': User
}


class DBStorage:
    """ Class DB Storage for Student Platform """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize storage instance
        """
        if getenv("NERVENEX_ENV") == "test":
            # Use test database
            user = "nervenex_test"
            password = "nervenex_test_pwd"
            host = "localhost"
            port = 3306
            db = "nervenex_test_db"
        else:
            # Use development database
            user = "nervenex_dev"
            password = "nervenex_dev_pwd"
            host = "localhost"
            port = 3306
            db = "nervenex_dev_db"

        engine_url = "mysql+mysqldb://{}:{}@{}:{}/{}".format(
                      user, password, host, port, db)
        self.__engine = create_engine(engine_url, pool_pre_ping=True,
                                      echo=False)

    def all(self, cls=None):
        """Query on the current database session all objects of the given class
            If cls is None: queries all types of objects.
            Return:
                Dict of queried classes in the format:
                <class name>.<obj id> = obj.
        """
        objs = []
        if cls is None:
            for a_class in classes.values():
                objs += self.__session.query(a_class)\
                        .order_by(a_class.id)\
                        .all()
        elif cls in classes.values():
                objs = self.__session.query(cls)\
                        .order_by(cls.id)\
                        .all()
        else:
            return dict()

        # Modify objects so that the result will be a dictionary of
        # key, value pairs where
        # key = <class name>.<object id>
        # value = object
        objs_dict = dict()
        for value in objs:
            key = type(value).__name__ + '.' + value.id
            objs_dict.update({key: value})

        return objs_dict

    def new(self, obj):
        """ add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database &
            the current database session
        """
        Base.metadata.create_all(self.__engine)

        # Create current database session
        # The option expire_on commit must be False
        # and scoped_session is used to ensur the session is thread-safe
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)  # global scope
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ close working session"""
        self.__session.close()

    def get(self, cls, id):
        """ Returns the object based on the class name and its ID, or
            None if not found
        """
        cls_list = list(classes.values())
        if cls not in cls_list:
            return (None)

        obj = self.__session.query(cls).filter(cls.id == id)
        if not obj:
            return (None)
        return (obj)

    def count(self, cls=None):
        """
        count the number of objects in storage
        - cls: the class to count its objects 'not string'
        """
        count = 0

        if cls is None:
            for a_class in classes.values():
                obj = self.__session.query(a_class).all()
                count += len(obj)
        else:
            obj = self.__session.query(cls).all()
            count = len(obj)

        return (count)
