#!/usr/bin/python3

"""The Thread class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Thread(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "threads"
        title = Column(String(128), nullable=False)
        author_id = Column(String(60),
                           ForeignKey("users.id", ondelete="CASCADE"))
        author = relationship("User", backref="threads")
        created_at = Column(DateTime, default=datetime.utcnow)
    else:
        title = ""
        author_id = ""
        author = None
        created_at = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
