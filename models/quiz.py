#!/usr/bin/python3

"""The Quiz class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class Quiz(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "quizzes"
        quiz_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        title = Column(String(255), nullable=False)
        description = Column(Text, nullable=True)
        duration = Column(Integer, nullable=False)
        is_active = Column(Boolean, default=False)
        questions = relationship("Question", backref="quiz")
    else:
        quiz_id = 0
        title = ""
        description = ""
        duration = 0
        is_active = False
        questions = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)