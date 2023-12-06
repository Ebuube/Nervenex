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
        author_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        thread_id = Column(String(60), ForeignKey("threads.id"),
                           nullable=False)

        # Relationships
        comments = relationship("Comment", backref="post")
    else:
        content = ""
        author_id = ""
        thread_id = ""

        @property
        def author(self):
            """
            Return a 'User' instance linked to this post
            """
            from models.user import User

            key = User.__name__ + '.' + self.author_id
            user = models.storage.all(User).get(key, None)

            return user

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance
        """
        super().__init__(*args, **kwargs)
