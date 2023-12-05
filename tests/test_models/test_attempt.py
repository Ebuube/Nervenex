#!/usr/bin/python3
"""
Tests for the Attempt model
"""
from tests.test_models.test_base_model import test_BaseModel
from models.attempt import Attempt


class test_Attempt(test_BaseModel):
    """
    Define extra tests for the ``Attempt`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        super().__init__(*args, **kwargs)

    def test_attempt_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        Namely:
        - quiz_id -> The quiz it is referencing
        - score -> How many questions the user got right
        - user_id -> The user who took the quiz
        - duration -> Time in minutes spent by the user
        - answers : all the answers given by the user.
        """
        _cls = Attempt

        foo = _cls()
        attrs = {
                'quiz_id': str, 'score': int, 'answers': list,
                'user_id': str
                }

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
