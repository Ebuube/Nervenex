#!/usr/bin/python3
"""
Defining FileStorage Class for Student Platform
"""

import json
import os
from models.base_model import BaseModel
from models.answer import Answer
from models.attempt import Attempt
from models.comment import Comment
from models.post import Post
from models.question import Question
from models.quiz import Quiz
from models.thread import Thread
from models.user import User


classes = {
            "BaseModel": BaseModel, "Answer": Answer, "Attempt": Attempt,
            "Comment": Comment, "Post": Post, "Question": Question,
            "Quiz": Quiz, "Thread": Thread, "User": User}


class FileStorage:
    """
    Class for Serializing and Deserializing Student Platform Data
    Class Attributes:
        __file_path - string with JSON file path ('file.json')
    """

    __file_path = "file.json"
    """Path to the JSON file"""
    __objects = {}
    """Empty dictionary to store all objects by <class name>.id"""

    def all(self, cls=None):
        """
        Returns the dictionary __objects, optionally filtered by class
        :param cls: Optional class to filter by
        :return: Dictionary of objects
        """

        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if type(value) is cls:
                    new_dict[key] = value
            return new_dict

        return self.__objects

    def new(self, obj):
        """
        Sets the obj in __objects with key <obj class name>.id
        :param obj: Object to add to storage
        """

        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        :return: None
        """

        newdict_objs = {}
        with open(self.__file_path, 'w') as json_f:
            for key, val in self.__objects.items():
                newdict_objs[key] = val.to_dict()
            json_f.write(json.dumps(newdict_objs))

    def delete(self, obj=None):
        """
        Removes the specified object from storage
        :param obj: Object to delete from storage
        :return: None
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def reload(self):
        """
        Deserializes the JSON file to __objects
        :return: None
        """

        temp = {}
        try:
            with open(self.__file_path, 'r') as json_f:
                temp = json.load(json_f)
                for key, val in temp.items():
                    self.__objects[key] = classes[val['__class__']](**val)
        except FileNotFoundError as e:
            # print("Error reloading data from file:", e)
            pass

    def get(self, cls, id):
        """
        Retrieves an object from storage based on its class and ID
        :param cls: Class of the object to retrieve
        :param id: ID of the object to retrieve
        :return: Object instance, or None if not found
        """
        if cls not in classes.values():
            return None

        try:
            key = cls.__name__ + "." + id
            if key in self.__objects:
                return self.__objects[key]
        except Exception as e:
            print("Error getting object from storage:\n", e)

    def count(self, cls=None):
        """
        Counts the number of objects in storage, optionally filtered by class
        :param cls: Optional class to filter by
        :return: Number of objects
        """
        if cls is not None:
            count = 0
            for key, val in self.__objects.items():
                if type(val) is cls:
                    count += 1
            return count
        else:
            return len(self.__objects)
