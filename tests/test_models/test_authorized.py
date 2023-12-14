#!/usr/bin/python3
"""
Tests for the Authorized model
"""
import models
from unittest import skipIf
from tests.test_models.test_base_model import test_BaseModel
from models.authorized import Authorized


class test_Authorized(test_BaseModel):
    """
    Define extra tests for the ``Authorized`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        super().__init__(*args, **kwargs)

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_authorized_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        Namely:
        - user_id -> Id of a logged in User
        """
        _cls = Authorized

        foo = _cls()
        attrs = {'user_id': str}

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
