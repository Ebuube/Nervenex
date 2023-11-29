#!/usr/bin/python3

"""The Post class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Post(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "posts"
        content = Column(String(255), nullable=False)
        author_id = Column(String(60), ForeignKey("users.id", ondelete="CASCADE"))
        author = relationship("User", backref="posts")
        created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        