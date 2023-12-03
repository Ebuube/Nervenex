#!/usr/bin/python3

"""The Attempt class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Attempt(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "attempts"
        attempt_id = Column(Integer, primary_key=True, autoincrement=True,
                            nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"),
                         ondelete="CASCADE", nullable=False)
        quiz_id = Column(Integer, ForeignKey("quizzes.id"),
                         ondelete="CASCADE", nullable=False)
        score = Column(Integer, nullable=False)
        total_questions = Column(Integer, nullable=False)
        start_time = Column(DateTime, default=datetime.utcnow)
        end_time = Column(DateTime, nullable=False)
        user = relationship("User", backref="attempts")
        quiz = relationship("Quiz", backref="attempts")
        answers = relationship("Answer", backref="attempt")
    else:
        attempt_id = 0
        user_id = 0
        quiz_id = 0
        score = 0
        total_questions = 0
        start_time = 0
        end_time = 0
        user = None
        answer = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
