#!/usr/bin/python3

"""The Quiz class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import (Column, Integer, String, DateTime, Boolean, ForeignKey,
                        Text)
from sqlalchemy.orm import relationship


class Quiz(BaseModel, Base):
    """
    Description of the Quiz class
    - is_active -> attribute
        It determines whether or not a quiz is available for other users.
        If True, then it will be globally accessible,
        else only the owner can see and modify it.

    """
    if models.storage_t == 'db':
        __tablename__ = "quizzes"
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        category_id = Column(String(60), ForeignKey('categories.id'),
                             nullable=False)
        title = Column(String(60), nullable=False)
        description = Column(Text, nullable=True)
        duration = Column(Integer, nullable=False)
        is_active = Column(Boolean, default=False)

        # Relationship
        questions = relationship("Question", backref="quiz")
        attempts = relationship("Attempt", backref="attempts")
    else:
        user_id = ""
        category_id = ""
        title = ""
        description = ""
        duration = 0    # How long (minutes) a quiz should last
        is_active = False
        question_ids = []

        @property
        def author(self):
            """
            Return a 'User' instance linked to this 'Quiz' instance
            """
            from models.user import User

            key = User.__name__ + '.' + self.user_id
            user = models.storage.all(User).get(key, None)

            return user

    def __init__(self, *args, **kwargs):
        """
        Initialize using Parent class
        """
        super().__init__(*args, **kwargs)
