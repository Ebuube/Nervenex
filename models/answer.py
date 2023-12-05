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
    value: Mathing 1-4 to a-d options
    """
    if models.storage_t == 'db':
        __tablename__ = "answers"
        # answer_id = Column(Integer, primary_key=True, autoincrement=True,
        #                    nullable=False)
        question_id = Column(String(60), ForeignKey("questions.id"),
                             ondelete="CASCADE", nullable=False)
        attempt_id = Column(String(60), ForeignKey("attempts.id"),
                            ondelete="CASCADE", nullable=False)
        value = Column(Integer, nullable=False)

        # Relationships
        question = relationship("Question", backref="answers")

        # Constraints
        # constrain `value` to 1-4 integer limit
    else:
        # answer_id = 0
        # user_id = ""
        # selected_option = 0
        # is_correct = False
        # created_at = None
        # question = None
        # user = None
        question_id = ""
        attempt_id = ""
        value = 0   # 1: 'a', 2: 'b', 3: 'c', 4: 'd'

    def __init__(self, *args, **kwargs):
        """
        Initialize instance
        """
        super().__init__(*args, **kwargs)
