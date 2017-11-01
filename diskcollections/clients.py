import os

from diskcollections.interfaces import IClient
from diskcollections.py2to3 import (
    basestring,
    TemporaryDirectory
)


class TemporaryFileClient(IClient):
    """Client that stores content in temporary directory.

    Temporary directory is created when client was initialized.
    Every new key are stored as file, with filename the same as key,
    in this directory.
    Temporary directory is removed when client is removed itself
    by garbage collector.
    Every new object creates new temporary directory.
    """

    def __init__(self):
        self.__string_keys = {}
        self.__directory = TemporaryDirectory()

    def __del__(self):
        self.__directory.cleanup()

    def __get_file_path(self, key):
        directory_path = self.__directory.name
        file_path = os.path.join(directory_path, key)
        return file_path

    def set(self, key, content):
        mode = 'wb'
        path = self.__get_file_path(key)

        if isinstance(content, basestring):
            mode = 'w'
            self.__string_keys[key] = True

        with open(path, mode=mode) as f:
            f.write(content)

    def get(self, key):
        mode = 'rb'
        path = self.__get_file_path(key)

        if not os.path.exists(path):
            raise KeyError(key)

        if key in self.__string_keys:
            mode = 'r'

        with open(path, mode=mode) as f:
            return f.read()

    def delete(self, key):
        file_path = self.__get_file_path(key)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise KeyError(key)

        self.__string_keys.pop(key, None)
