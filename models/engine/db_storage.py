#!/usr/bin/python3
"""
DB Storage for Student Platform
"""

from models.base_model import BaseModel, Base
from models.user import User
from models.quiz import Quiz
from models.question import Question
from models.answer import Answer
from models.attempt import Attempt
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    'User': User,
    'Quiz': Quiz,
    'Question': Question,
    'Answer': Answer,
    'Attempt': Attempt
}


class DBStorage:
    """ Class DB Storage for Student Platform """
    __engine = None
    __session = None

    def __init__(self):
        user = "student_platform_dev"
        password = "student_platform_pwd"
        host = "localhost"
        db = "student_platform_db"

        self.__engine = create_engine(
                "mysql+mysqldb://{}:{}@{}/{}".format(user, password, host, db))

    def all(self, cls=None):
        """Query on the current database session all objects of the given class
            If cls is None: queries all types of objects.
            Return:
                Dict of queried classes in the format:
                <class name>.<obj id> = obj.
        """
        new_list = []
        if cls is None:
            for clss in classes:
                new_list.extend(self.__session.query(classes[clss]).all())
        else:
            if cls in classes.values():
                new_list = self.__session.query(cls)

        return ({}.format(type(obj).__name__, obj.id): obj for obj in new_list)

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
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
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
        """
        count = 0

        if not cls:
            for clss in classes:
                obj = self.__session.query(eval(clss)).all()
                count += len(obj)
        else:
            obj = self.__session.query(classes[cls]).all()
            count = len(obj)

        return (count)
