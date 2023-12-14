#!/usr/bin/python3
import models
from models.user import User
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

class Authorized(BaseModel, Base):
    """
    Keeps a record of the logged in users
    """
    __tablename__ = 'authorized'
    if models.storage_t == 'db':
        user_id = Column(String(60), nullable=False, unique=True)
    else:
        user_id = ""

    @staticmethod
    def is_auth(user):
        """
        Check if a user is currently logged in or not
        """
        for auth in models.storage.all(Authorized).values():
            if auth.user_id == user.id:
                return True

        return False

    @staticmethod
    def remove(user):
        """
        Unauthorize a user

        Return:
            True: if user was found and unauthorized
            False: if user was not found
        """
        for auth in models.storage.all(Authorized).values():
            if auth.user_id == user.id:
                auth.delete()
                models.storage.save()
                return True

        return False

    @staticmethod
    def add(user):
        """
        Authorize a user
        - If user is already authorized, the authorization is renewed
        """
        for auth in models.storage.all(Authorized).values():
            if auth.user_id == user.id:
                auth.save()
                return

        new = Authorized()
        new.user_id = user.id
        new.save()
