#!/usr/bin/python3

"""The Question class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship


class Question(BaseModel, Base):
    """
    Logic: Prevent addition of extra questions, change of duration \
            once quiz is uploaded
    but permit modification of the questions
    """
    if models.storage_t == 'db':
        __tablename__ = "questions"
        quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
        quiz = relationship("Quiz", backref="questions")
        text = Column(String(255), nullable=False)
        option_a = Column(String(255), nullable=False)
        option_b = Column(String(255), nullable=False)
        option_c = Column(String(255), nullable=False)
        option_d = Column(String(255), nullable=False)
        correct_answer = Column(Integer, nullable=False)
    else:
        quiz_id = ""
        text = ""
        option_a = ""
        option_b = ""
        option_c = ""
        option_d = ""
        # correct_answer = 0    # Not needed

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
