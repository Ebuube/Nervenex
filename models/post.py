#!/usr/bin/python3

"""The Post class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Post(BaseModel, Base):
    """
    Posts made by users
    - content : what the post is all about
    - author_id : id of user who made the post
    - thread_id : id of thread under which the post was made
    """
    if models.storage_t == 'db':
        __tablename__ = "posts"
        content = Column(Text, nullable=False)
        author_id = Column(String(60), ForeignKey("users.id"))
        thread_id = Column(String(60), ForeignKey("threads.id"))

        # Relationships
    else:
        content = ""
        author_id = ""
        thread_id = ""

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance
        """
        super().__init__(*args, **kwargs)
