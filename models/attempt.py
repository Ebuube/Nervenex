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
        user_id = Column(String(60), ForeignKey("users.id"),
                         ondelete="CASCADE", nullable=False)
        quiz_id = Column(Integer, ForeignKey("quizzes.id"),
                         ondelete="CASCADE", nullable=False)
        score = Column(Integer, nullable=False)
        duration = Column(Integer, nullable=False)

        # Relationships
        user = relationship("User", backref="attempts")
        quiz = relationship("Quiz", backref="attempts")
        answers = relationship("Answer", backref="attempt")
    else:
        # attempt_id = 0
        user_id = ""
        quiz_id = ""
        score = 0
        duration = 0
        answer_ids = []
        # user = None   \t should be implemented as a property method
        # answers -> A property

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
