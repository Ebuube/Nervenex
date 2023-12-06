#!/usr/bin/python3
"""
The Category class to identify types of data
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """
    The Category class identifies data of different types
    """
    if models.storage_t == 'db':
        __tablename__ = "categories"
        name = Column(String(128), unique=True, nullable=False)

        # Relationships
        threads = relationship("Thread", backref="category")
        quizzes = relationship("Quiz", backref="category")
    else:
        name = ""

        @property
        def quizzes(self):
            """
            Return a list of Quiz instances linked to this category
            """
            from models.quiz import Quiz

            objs = []
            for quiz in models.storage.all(Quiz).values():
                if quiz.category_id == self.id:
                    objs.append(quiz)

            return objs

        @property
        def threads(self):
            """
            Return a list of Thread instances linked to this category
            """
            from models.thread import Thread

            objs = []
            for thread in models.storage.all(Thread).values():
                if thread.category_id == self.id:
                    objs.append(thread)

            return objs

    def __init__(self, *args, **kwargs):
        """
        Initialize using the Parent class
        """
        super().__init__(*args, **kwargs)
