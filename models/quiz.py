#!/usr/bin/python3

"""The Quiz class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class Quiz(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "quizzes"
        quiz_id = Column(Integer, primary_key=True, autoincrement=True,
                         nullable=False)
        title = Column(String(255), nullable=False)
        description = Column(Text, nullable=True)
        duration = Column(Integer, nullable=False)
        is_active = Column(Boolean, default=False)
        questions = relationship("Question", backref="quiz")
    else:
        # quiz_id = ""
        title = ""
        description = ""
        duration = 0    # How long (minutes) a quiz should last
        # is_active -> attribute
        # It determines whether or not a quiz is available for other users.
        # If True, then it will be globally accessible,
        # else only the owner can see and modify it.
        is_active = False
        questions = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
