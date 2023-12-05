#!/usr/bin/python3

"""The Post class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
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
        content = Column(String(255), nullable=False)
        author_id = Column(String(60),
                           ForeignKey("users.id", ondelete="CASCADE"))
        author = relationship("User", backref="posts")
        created_at = Column(DateTime, default=datetime.utcnow)
    else:
        content = ""
        author_id = ""
        # author = None # Will be a property method
        # created_at = None
        thread_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
