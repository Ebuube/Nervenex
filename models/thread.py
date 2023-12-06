#!/usr/bin/python3

"""The Thread class that inherits from BaseModel"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Thread(BaseModel, Base):
    """
    A discussion topic
    - title : title of discussion
    - author_id : id of user who created the thread
    """
    if models.storage_t == 'db':
        __tablename__ = "threads"
        title = Column(String(128), nullable=False)
        author_id = Column(String(60), ForeignKey("users.id"))

        # Relationships
    else:
        title = ""
        author_id = ""

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance
        """
        super().__init__(*args, **kwargs)
