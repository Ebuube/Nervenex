#!/usr/bin/python3
"""user class"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5
from models.quiz import Quiz
from models.attempt import Attempt
from models.post import Post
from models.comment import Comment


class User(BaseModel, Base):
    """The User class that inherits from BaseModel"""
    if models.storage_t == 'db':
        __tablename__ = "users"
        email = Column(String(128), nullable=False, unique=True)
        password = Column(String(60), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)

        # Relationships
        quizzes = relationship("Quiz", backref="author")
        attempts = relationship("Attempt", backref="maker")
        posts = relationship("Post", backref="author")
        comments = relationship("Comment", backref="author")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        @property
        def quizzes(self):
            """
            Return a list of 'Quiz' instances linked to this User instance
            """
            objs = list()
            for quiz in models.storage.all(Quiz).values():
                if quiz.user_id == self.id:
                    objs.append(quiz)

            return objs

        @property
        def attempts(self):
            """
            Return a list of 'Attempt'  instances linked to this User
            instance
            """
            objs = list()
            for attempt in models.storage.all(Attempt).values():
                if attempt.user_id == self.id:
                    objs.append(attempt)

            return objs

        @property
        def posts(self):
            """
            Return a list of 'Post' instances linked to this User
            instance
            """
            objs = list()
            for post in models.storage.all(Post).values():
                if post.author_id == self.id:
                    objs.append(post)

            return objs

        @property
        def comments(self):
            """
            Return a list of 'Comment' instances linked to this User
            instance
            """
            objs = list()
            for comment in models.storage.all(Comment).values():
                if comment.author_id == self.id:
                    objs.append(comment)

            return objs

    def __init__(self, *args, **kwargs):
        """
        Initialize instance
        """
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """set password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
