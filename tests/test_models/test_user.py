#!/usr/bin/python3
"""
Tests for the User model
"""
from tests.test_models.test_base_model import test_BaseModel
from models.user import User


class test_User(test_BaseModel):
    """
    Define extra tests for the ``User`` class
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of the class' test
        """
        super().__init__(*args, **kwargs)
        self.value = User
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

    def test_user_attrs(self):
        """
        Ensure that the correct attributes are present in the model
        Namely:
        - email -> string
        - password -> string
        - first_name -> string
        - last_name -> string
        """
        _cls = User

        foo = _cls()
        attrs = {'email': str, 'password': str, 'first_name': str,
                 'last_name': str}

        for attr, attr_type in attrs.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                self.assertTrue(hasattr(foo, attr))
                self.assertEqual(type(getattr(foo, attr)), attr_type)
