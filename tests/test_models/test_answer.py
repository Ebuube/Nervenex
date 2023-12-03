#!/usr/bin/python3
"""
Tests for the Answer model
"""
from tests.test_models.test_base_model import test_BaseModel
from models.answer import Answer


class test_Answer(test_BaseModel):
    """
    Define extra tests for the ``Answer`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        super().__init__(*args, **kwargs)

    def test_answer_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        Namely:
        - value -> The correct option amongst (1: 'a', 2: 'b', 3: 'c', 4: 'd')
        - explanation -> A reason for the answer
        - question_id -> The particular question it references
        """
        _cls = Answer

        foo = _cls()
        attrs = {
                'value': int, 'explanation': str, 'question_id': str
                }

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
