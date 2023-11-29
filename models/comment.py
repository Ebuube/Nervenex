#!/usr/bin/python3

"""The Comment class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Comment(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "comments"
        content = Column(String(255), nullable=False)
        post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
        post = relationship("Post", backref="comments")
        author_id = Column(String(60), ForeignKey("users.id", ondelete="CASCADE"))
        author = relationship("User", backref="comments")
        created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)