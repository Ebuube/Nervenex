#!/usr/bin/python3

"""The Answer class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Text)
from sqlalchemy.orm import relationship


class Answer(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "answers"
        answer_id = Column(Integer, primary_key=True, autoincrement=True,
                           nullable=False)
        question_id = Column(Integer, ForeignKey("questions.id"),
                             ondelete="CASCADE", nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"),
                         ondelete="CASCADE", nullable=False)
        selected_option = Column(Integer, nullable=False)
        is_correct = Column(Boolean, nullable=False)
        explanation = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        question = relationship("Question", backref="answers")
        user = relationship("User", backref="answers")
    else:
        # answer_id = 0
        # user_id = ""
        # selected_option = 0
        # is_correct = False
        # created_at = None
        # question = None
        # user = None
        question_id = ""
        explanation = ""
        value = 0   # 1: 'a', 2: 'b', 3: 'c', 4: 'd'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
