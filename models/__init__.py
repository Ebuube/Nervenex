#!/usr/bin/python3
"""
initialize the models package
Environmental variables considered:
    NERVENEX_TYPE_STORAGE -> 'db' or (anything else taken as file storage)
    NERVENEX_ENV -> 'dev' or 'test'
"""

from os import getenv


storage_t = getenv("NERVENEX_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
