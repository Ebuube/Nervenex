#!/usr/bin/python3
"""
Tests for the Resource model
"""
import models
from unittest import skipIf
from tests.test_models.test_base_model import test_BaseModel
from models.resource import Resource


class test_Resource(test_BaseModel):
    """
    Define extra tests for the ``Resource`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        super().__init__(*args, **kwargs)

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_resource_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        """
        _cls = Resource

        foo = _cls()
        attrs = {
                'title': str, 'author_id': str, 'type': str,
                'link': str, 'description': str
                }

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
