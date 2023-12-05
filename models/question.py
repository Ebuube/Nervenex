#!/usr/bin/python3

"""The Question class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.orm import relationship


class Question(BaseModel, Base):
    """
    Logic: Prevent addition of extra questions, change of duration \
            once quiz is uploaded
    but permit modification of the questions
    """
    if models.storage_t == 'db':
        __tablename__ = "questions"
        quiz_id = Column(String(60),
                         ForeignKey("quizzes.id", ondelete="CASCADE"))
        content = Column(Text, nullable=False)
        option_a = Column(String(128), nullable=False)
        option_b = Column(String(128), nullable=False)
        option_c = Column(String(128), nullable=False)
        option_d = Column(String(128), nullable=False)
        # correct_answer = Column(Integer, nullable=False)

        # Relationships
        quiz = relationship("Quiz", backref="questions")
    else:
        quiz_id = ""
        content = ""
        option_a = ""
        option_b = ""
        option_c = ""
        option_d = ""
        # correct_answer = 0    # Not needed

    def __init__(self, **kwargs):
        """
        Initialize the instance
        """
        super().__init__(**kwargs)
