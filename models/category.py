#!/usr/bin/python3
"""
The Category class to identify types of data
"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """
    The Category class identifies data of different types
    """
    if models.storage_t == 'db':
        __tablename__ = "categories"
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        Initialize using the Parent class
        """
        super().__init__(*args, **kwargs)
