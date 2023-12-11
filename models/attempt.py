#!/usr/bin/python3

"""The Attempt class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Attempt(BaseModel, Base):
    """
    Definition of the `Attempt` class
    - quiz_id : The quiz it is referencing
    - user_id : The user who took the quiz
    - score : number of correct answers
    - duration : how long the user spent (in minutes)
    - answers : all the answers given by the user.
    """
    if models.storage_t == 'db':
        __tablename__ = "attempts"
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        quiz_id = Column(String(60), ForeignKey("quizzes.id"), nullable=False)
        score = Column(Integer, nullable=False)
        duration = Column(Integer, nullable=False)

        # Relationships
        answers = relationship("Answer", backref="attempt", cascade="delete")
    else:
        user_id = ""
        quiz_id = ""
        score = 0
        duration = 0
        answer_ids = []

        @property
        def maker(self):
            """
            Return a 'User' instance linked to this Attempt instance
            """
            from models.user import User

            key = User.__name__ + '.' + self.user_id
            user = models.storage.all(User).get(key, None)

            return user

        @property
        def quiz(self):
            """
            Return a Quiz instance linked to this Attempt
            """
            from models.quiz import Quiz

            key = Quiz.__name__ + '.' + self.quiz_id
            obj = models.storage.all(Quiz).get(key, None)

            return obj

        @property
        def answers(self):
            """
            Return a list of 'Answer' instances linked to this Attempt instance
            """
            from models.answer import Answer

            objs = list()
            for answer in models.storage.all(Answer).values():
                if answer.attempt_id == self.id:
                    objs.append(answer)

            return objs

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance
        """
        super().__init__(*args, **kwargs)
