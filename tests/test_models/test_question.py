#!/usr/bin/python3
"""
Tests for the Question model
"""
from tests.test_models.test_base_model import test_BaseModel
from models.question import Question


class test_Question(test_BaseModel):
    """
    Define extra tests for the ``Question`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        # print("\nTesting Question\n")   # test
        super().__init__(*args, **kwargs)

    def test_question_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        Namely:
        - quiz_id -> id of the Quiz it is classified under
        - text -> A descripion of the question to answer
        - option_a -> First option
        - option_b -> Second option
        - option_c -> Third option
        - option_d -> Fourth option
        """
        _cls = Question

        foo = _cls()
        attrs = {
                    'quiz_id': str, 'text': str, 'option_a': str,
                    'option_b': str, 'option_c': str, 'option_d': str
                }

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
