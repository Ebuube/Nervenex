#!/usr/bin/python3
"""
Tests for the Quiz model
"""
from tests.test_models.test_base_model import test_BaseModel
from models.quiz import Quiz


class test_Quiz(test_BaseModel):
    """
    Define extra tests for the ``Quiz`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        # print("\nTesting Quiz\n")   # test
        super().__init__(*args, **kwargs)

    def test_quiz_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        Namely:
        - title -> string
        - description -> string
        - duration -> integer   # Represents time in minutes
        - is_active -> Boolean  # Determines if quiz is globally accessible
        - questions -> A list of strings : ids of questions under it
        """
        _cls = Quiz

        foo = _cls()
        attrs = {
                    'title': str, 'description': str,
                    'duration': int, 'is_active': bool, 'questions': list
                }

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
