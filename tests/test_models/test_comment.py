#!/usr/bin/python3
"""
Tests for the Comment model
"""
import models
from unittest import skipIf
from tests.test_models.test_base_model import test_BaseModel
from models.comment import Comment


class test_Comment(test_BaseModel):
    """
    Define extra tests for the ``Comment`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        super().__init__(*args, **kwargs)

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_comment_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        """
        _cls = Comment

        foo = _cls()
        attrs = {
                'content': str, 'author_id': str, 'post_id': str
                }

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
