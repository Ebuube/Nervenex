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
        post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
        post = relationship("Post", backref="comments")
        author_id = Column(String(60), ForeignKey("users.id",
                           ondelete="CASCADE"))
        author = relationship("User", backref="comments")
        created_at = Column(DateTime, default=datetime.utcnow)
    else:
        content = ""
        post_id = ""
        author_id = ""
        # post = None # property method
        # author = None # property method
        # created_at = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
