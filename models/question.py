#!/usr/bin/python3

"""The Question class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship


class Question(BaseModel, Base):
    """
    Logic: Prevent addition of extra questions, change of duration \
            once quiz is uploaded
    but permit modification of the questions
    correct_answer -> from 1-4 matching options a-d
    """
    if models.storage_t == 'db':
        __tablename__ = "questions"
        quiz_id = Column(String(60), ForeignKey("quizzes.id"), nullable=False)
        content = Column(Text, nullable=False)
        option_a = Column(String(128), nullable=False)
        option_b = Column(String(128), nullable=False)
        option_c = Column(String(128), nullable=False)
        option_d = Column(String(128), nullable=False)
        correct_answer = Column(Integer, nullable=False)
        explanation = Column(Text, nullable=True)

        # Relationships
        answers = relationship("Answer", backref="question")
    else:
        quiz_id = ""
        content = ""
        option_a = ""
        option_b = ""
        option_c = ""
        option_d = ""
        correct_answer = 0
        explanation = ""

        @property
        def answers(self):
            """
            Return a list of Answer instances linked to this Question
            """
            from models.answer import Answer

            objs = list()
            for answer in models.storage.all(Answer).values():
                if answer.question_id == self.id:
                    objs.append(answer)

            return objs

        @property
        def quiz(self):
            """
            Return a Quiz instance linked to this question
            """
            from models.quiz import Quiz

            key = Quiz.__name__ + '.' + self.quiz_id
            obj = models.storage.all(Quiz).get(key, None)

            return obj

    def __init__(self, **kwargs):
        """
        Initialize the instance
        """
        super().__init__(**kwargs)
