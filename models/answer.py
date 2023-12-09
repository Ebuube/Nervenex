#!/usr/bin/python3

"""The Answer class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Text)
from sqlalchemy.orm import relationship


class Answer(BaseModel, Base):
    """
    Description of answer to a question
    This is the answer supplied by the quiz-taker not creator.
    value: Mathing 1-4 to a-d options
    """
    if models.storage_t == 'db':
        __tablename__ = "answers"
        question_id = Column(String(60), ForeignKey("questions.id"),
                             nullable=False)
        attempt_id = Column(String(60), ForeignKey("attempts.id"),
                            nullable=False)
        value = Column(Integer, nullable=False)

        # Constraints
        # constrain `value` to 1-4 integer limit
    else:
        question_id = ""
        attempt_id = ""
        value = 0   # 1: 'a', 2: 'b', 3: 'c', 4: 'd'

        @property
        def attempt(self):
            """
            Return an 'Attempt' instance linked to this Answer instance
            """
            from models.attempt import Attempt

            key = Attempt.__name__ + '.' + self.attempt_id
            obj = models.storage.all(Attempt).get(key, None)

            return obj

        @property
        def question(self):
            """
            Return a 'Question' instance linked to this Answer instance
            """
            from models.question import Question

            key = Question.__name__ + '.' + self.question_id
            obj = models.storage.all(Question).get(key, None)

            return obj

    def __init__(self, *args, **kwargs):
        """
        Initialize instance
        """
        super().__init__(*args, **kwargs)
