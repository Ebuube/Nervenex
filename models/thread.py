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
        author_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        category_id = Column(String(60), ForeignKey("categories.id"),
                             nullable=False)

        # Relationships
        posts = relationship("Post", backref="thread", cascade="delete")
    else:
        title = ""
        author_id = ""
        category_id = ""

        @property
        def author(self):
            """
            Return a User instances linked to this Thread
            """
            from models.user import User

            key = User.__name__ + '.' + self.author_id
            obj = models.storage.all(User).get(key, None)

            return obj

        @property
        def category(self):
            """
            Return a Category instance linked to this Thread
            """
            from models.category import Category

            key = Category.__name__ + '.' + self.category_id
            obj = models.storage.all(Category).get(key, None)

            return obj

        @property
        def posts(self):
            """
            Return a list of Post instances linked to this Thread
            """
            from models.post import Post

            objs = []
            for post in models.storage.all(Post).values():
                if post.thread_id == self.id:
                    objs.append(post)

            return objs

    def __init__(self, *args, **kwargs):
        """
        Initialize an instance
        """
        super().__init__(*args, **kwargs)
