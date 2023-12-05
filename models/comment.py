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
        post_id = Column(String(60),
                         ForeignKey("posts.id", ondelete="CASCADE"))
        author_id = Column(String(60), ForeignKey("users.id",
                           ondelete="CASCADE"))

        # Relationships
        post = relationship("Post", backref="comments")
        author = relationship("User", backref="comments")
    else:
        content = ""
        post_id = ""
        author_id = ""
        # post = None # property method
        # author = None # property method
        # created_at = None

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance
        """
        super().__init__(*args, **kwargs)
