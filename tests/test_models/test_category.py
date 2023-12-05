#!/usr/bin/python3
"""
Tests for the Category class
"""
from tests.test_models.test_base_model import test_BaseModel
from models.category import Category


class test_Category(test_BaseModel):
    """
    Define extra tests for the ``User`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the test
        """
        super().__init__(*args, **kwargs)
        self.value = Category
        self.name = self.value.__name__

    def setUp(self):
        """
        Set up for tests
        """
        super().setUp()

    def tearDown(self):
        """
        Tear down for the tests
        """
        super().tearDown()

    def test_category_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        Namely:
        - name -> string
        """
        _cls = Category

        foo = _cls()
        attrs = {'name': str}

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
