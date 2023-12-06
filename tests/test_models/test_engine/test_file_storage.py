#!/usr/bin/python3
"""
Tests for the FileStorage class
"""
import os
import models
import unittest
import datetime
import pep8
from unittest import skipIf
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.answer import Answer
from models.attempt import Attempt
from models.category import Category
from models.comment import Comment
from models.post import Post
from models.question import Question
from models.quiz import Quiz
from models.thread import Thread
from models.user import User

from tests import config


class test_FileStorage(unittest.TestCase):
    """
    Define tests for the ``FileStorage`` class
    """
    # Set maxDiff to see all output on error comparison
    maxDiff = None

    def __init__(self, *args, **kwargs):
        """
        Initialize the test instance
        """
        super().__init__(*args, **kwargs)
        self.value = FileStorage
        self.name = self.value.__name__
        self.file_path = 'file.json'
        self._classes = [BaseModel, Answer, Attempt, Category, Comment, Post,
                         Question, Quiz, Thread, User]

    def setUp(self):
        """
        Set up the environment for each test method
        """
        # Remove previous storage files
        json_fmt = ".json"
        path = "./"     # path to work on

        for root, dirs, files in os.walk(path):
            for _file in files:
                if _file.endswith(json_fmt):
                    file_path = os.path.join(root, _file)
                    os.remove(file_path)
                    if config.setUp_verbose is True:
                        print("Removed: '{}'".format(file_path))

    def tearDown(self):
        """
        Tear down the environment after each test method
        """
        # Remove previous storage files
        json_fmt = ".json"
        path = "./"     # path to work on

        for root, dirs, files in os.walk(path):
            for _file in files:
                if _file.endswith(json_fmt):
                    file_path = os.path.join(root, _file)
                    os.remove(file_path)
                    if config.setUp_verbose is True:
                        print("Removed: '{}'".format(file_path))

    def test_check_pep8_compliance(self):
        """
        Ensure all '*.py' files are pep8 (or pycodestyle) compliant
        It is ran only ``once`` during a test
        """
        if config.pep8_checked is False:
            path = "./"
            style = pep8.StyleGuide(quite=False, show_source=True,
                                    verbose=config.pep8_verbose)
            result = style.check_files(paths=path)
            self.assertEqual(result.total_errors, 0, "Fix pep8")
            config.pep8_checked = True

    def test_file_path(self):
        """
        Ensure that the path for storage is a "*.json" string
        """
        # self.assertFalse(os.path.exists(self.file_path))
        self.assertFalse(os.path.exists(self.file_path))
        FileStorage().save()
        self.assertTrue(os.path.exists(self.file_path))

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_all(self):
        """
        Ensure that the ``all`` method is implemented
        Returns the dictionary '__objects'
        """
        storage = FileStorage()
        _cls = BaseModel
        self.assertTrue(hasattr(storage, 'all'))
        self.assertEqual(type(storage.all()), dict)

        # Objects
        foo = _cls()
        foo.save()
        bar = _cls()
        bar.save()
        key = type(foo).__name__ + '.' + foo.id
        self.assertEqual(foo, storage.all()[key])
        key = type(bar).__name__ + '.' + bar.id
        self.assertEqual(bar, storage.all()[key])

    def test_new(self):
        """
        Ensure that the ``new`` method is implemented
        Sets in '__objects' the 'obj' with key '<obj class name>.id'
        """
        storage = FileStorage()
        _cls = BaseModel
        self.assertTrue(hasattr(storage, 'new'))
        kwargs = {'id': '1234-1234-1234',
                  'created_at': datetime.datetime.now().isoformat(),
                  'updated_at': datetime.datetime.now().isoformat(),
                  'first_name': 'Edwin',
                  'last_name': 'Ebube'}
        foo = _cls(**kwargs)
        # Ensure object created from dictionary is not automaticall saved
        key = test_FileStorage.get_key(foo)
        self.assertNotIn(key, storage.all().keys())

        # Keep track of object
        storage.new(foo)
        self.assertIn(key, storage.all().keys())

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_save(self):
        """
        Ensure that the 'save' method is implemented
        Serializes '__objects' to the JSON file (path: __file_path)
        """
        storage = FileStorage()

        # These are individual tests for the classes
        # combined in one method.
        for _cls in self._classes:
            self.setUp()

            self.assertFalse(os.path.exists(self.file_path))

            # Empty objects
            storage.save()
            self.assertTrue(os.path.exists(self.file_path))

            # With some objects
            foo = _cls()
            bar = _cls()
            objs = [foo, bar]
            foo.save()
            bar.save()
            storage.save()

            for obj in objs:
                with self.subTest(obj=obj):
                    key = test_FileStorage.get_key(obj)
                    self.assertIn(key, storage.all().keys())
            self.tearDown()

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_reload(self):
        """
        Ensure that the 'reload' method is implemented
        Deserializes the JSON file to '__objects'
        Only if the JSON file (__file_path) exists;
        otherwise, do nothing.
        If the files doesn't exist, no exception should be raised
        """
        storage = FileStorage()

        # These are individual tests for the classes
        # combined in one method.
        for _cls in self._classes:
            self.setUp()

            self.assertFalse(os.path.exists(self.file_path))
            # The line of code below should not raise an error
            storage.reload()

            # Serialize some objects
            foo = _cls()
            bar = _cls()
            foo.save()
            bar.save()
            self.assertTrue(os.path.exists(self.file_path))

            # Deserialize some objects
            objs = [foo, bar]
            new_storage = FileStorage()
            new_storage.reload()

            for obj in objs:
                with self.subTest(obj=obj):
                    key = test_FileStorage.get_key(obj)
                    self.assertIn(key, new_storage.all().keys())

            self.tearDown()

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_delete(self):
        """
        Ensure that the 'delete' method is implemented
        Deletes an object from loaded storage
        """
        storage = FileStorage()

        # These are individual tests for the classes
        for _cls in self._classes:
            self.setUp()

            self.assertFalse(os.path.exists(self.file_path))
            # The line of code below should not raise an error
            storage.reload()

            # Create some objects
            foo = _cls()
            bar = _cls()
            foo.save()
            bar.save()
            self.assertTrue(os.path.exists(self.file_path))

            # Confirm objects were saved
            objs = [foo, bar]
            new_storage = FileStorage()
            new_storage.reload()

            # Delete objects
            for obj in objs:
                with self.subTest(obj=obj):
                    key = test_FileStorage.get_key(obj)
                    # print("Deleting obj: <{}>".format(key))
                    new_storage.delete(obj)
            new_storage.save()

            # Confirm changes are reflected in previous storage
            storage.reload()

            for obj in objs:
                storage_objs = storage.all()
                with self.subTest(obj=obj):
                    key = test_FileStorage.get_key(obj)
                    # print("Confirming absence: <{}>".format(key))
                    self.assertNotIn(key, storage_objs)

            self.tearDown()

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_get(self):
        """
        Ensure that the 'get' method is implemented
        Retrieves an object from storage based on its class and ID
        """
        storage = FileStorage()

        for _cls in self._classes:
            self.setUp()

            self.assertFalse(os.path.exists(self.file_path))
            # The line of code below should not raise an error
            storage.reload()

            # Create some objects
            foo = _cls()
            bar = _cls()
            foo.save()
            bar.save()
            self.assertTrue(os.path.exists(self.file_path))

            # Confirm objects were saved
            objs = [foo, bar]
            new_storage = FileStorage()
            new_storage.reload()

            # Get a particular object
            self.assertEqual(bar.id, storage.get(_cls, bar.id).id)

            self.tearDown()

    @skipIf(models.storage_t == 'db', "Test is for file storage")
    def test_count(self):
        """
        Ensure that the 'count' method is implemented
        Counts the number of objects in storage, optionally filtered by class
        """
        storage = FileStorage()
        initial = storage.count()
        # Create some objects
        foo = BaseModel()

        # Save them
        foo.save()
        self.assertEqual(1 + initial, storage.count())

    """
    Static methods
    """
    @staticmethod
    def get_key(obj):
        """
        Create 'storage' key for an object
        """
        key = None
        delim = '.'
        if hasattr(obj, 'id'):
            key = type(obj).__name__ + delim + obj.id
        else:
            raise Exception("Invalid argument to 'get_key()' method")

        return key

    @staticmethod
    def get_class_name(storage_key):
        """
        Extract class name from a 'storage' key
        """
        delim = '.'
        if type(storage_key) is str:
            name = storage_key.split(delim)[0]

        return name

    @staticmethod
    def get_obj_id(storage_key):
        """
        Extract object id from a 'storage' key
        """
        delim = '.'
        if type(storage_key) is str:
            name = storage_key.split(delim)[1]

        return name
