#!/usr/bin/python3
"""
Tests for the Thread model
"""
from tests.test_models.test_base_model import test_BaseModel
from models.thread import Thread


class test_Thread(test_BaseModel):
    """
    Define extra tests for the ``Thread`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        super().__init__(*args, **kwargs)

    def test_thread_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        """
        _cls = Thread

        foo = _cls()
        attrs = {
                'title': str, 'author_id': str
                }

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
