#!/usr/bin/python3
"""
The Resource class - inherits from BaseModel
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Resource(BaseModel, Base):
    """
    Learning Resources created by users for users
    - title: what the learning resources is all about
    - author_id: id of the user who created this learning resource
    - type: the type of learning resource: text, video
    - link: link to the learning resource
    - description: a brief description of what the resource can offer
    """
    if models.storage_t == 'db':
        __tablename__ = "resources"
        title = Column(String(30), nullable=False)
        author_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        type =  Column(String(6), nullable=False)
        link = Column(String(1000), nullable=False)
        description = Column(String(400), nullable=False)
    else:
        title = ""
        author_id = ""
        type = ""
        link = ""
        description = ""

        @property
        def author(self):
            """
            Return a 'User' instnace linked to this Learning Resource
            """
            from models.user import User

            key = User.__name__ + '.' + self.author_id
            obj = models.storage.all(User).get(key, None)

            return obj
