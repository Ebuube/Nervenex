#!/usr/bin/python3
"""user class"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


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
        attempts = relationsihp("Attempt", backref="maker")
        posts = relationship("Post", backref="author")
        comment = relationship("Comment", backref="author")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

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
