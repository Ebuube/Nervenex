#!/usr/bin/python3

"""The Comment class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Comment(BaseModel, Base):
    """
    Description of Comment's under a post
    - content : content of the comment
    - post_id : post it is referencing
    - author_id : id of user who made the comment
    """
    if models.storage_t == 'db':
        __tablename__ = "comments"
        content = Column(String(255), nullable=False)
        author_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        post_id = Column(String(60), ForeignKey("posts.id"), nullable=False)
    else:
        content = ""
        post_id = ""
        author_id = ""

        @property
        def author(self):
            """
            Return a 'User' instance linked to this comment
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
