import os.path
import tempfile
from typing import Optional

from diskcollections.interfaces import IClientSequence
from diskcollections.py2to3 import TemporaryDirectory

mode_str = "w+"
mode_bytes = "w+b"
modes = {mode_str, mode_bytes}


class TemporaryDirectoryClient(IClientSequence):
    """
    Client that stores every item in separated file in temporary directory.

    When client is removed, all files and directory are also removed.
    Client creates new file on every new item.
    If under index file exist, then file will be removed and created with
    new content.
    """

    def __init__(self, iterable=(), mode=mode_bytes):
        super(TemporaryDirectoryClient, self).__init__()
        self.__mode = mode
        self.__available_modes = modes - {mode}
        self.__files = []
        self.__directory = TemporaryDirectory()
        self.extend(iterable)

    def __repr__(self):
        return "TemporaryDirectoryClient(%s)" % self.__str__()

    def __str__(self):
        s = ", ".join(map(repr, self))
        return "[%s]" % s

    def __del__(self):
        for f in self.__files:
            f.close()
        self.__directory.cleanup()

    def __delitem__(self, index):
        del self.__files[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            start, stop, step = indices
            items = (self[i] for i in range(start, stop, step))
            return self.__class__(iterable=items, mode=self.__mode)

        file = self.__files[index]
        file.seek(0)
        return file.read()

    def __setitem__(self, index, value):
        file = self.safe_write(value)
        self.__files[index] = file

    def __len__(self):
        return len(self.__files)

    def insert(self, index, value):
        file = self.safe_write(value)
        self.__files.insert(index, file)

    def __write(self, value, mode: Optional[str] = None):
        mode = mode or self.__mode
        file = tempfile.TemporaryFile(mode=mode, dir=self.__directory.name)
        file.write(value)
        return file

    def safe_write(self, value):
        try:
            return self.__write(value)
        except TypeError:
            pass

        exc = None

        for mode in self.__available_modes:
            try:
                return self.__write(value, mode=mode)
            except TypeError as e:
                exc = e
        raise exc


class PersistentDirectoryClient(IClientSequence):
    """
    Client that stores every item in separated file in created directory.

    When client is removed, all files and directory are not removed.
    Client creates new file on every new item.
    If under index file exist, then file will be removed and created with
    new content.
    """

    def __init__(self, directory, iterable=()):
        super(PersistentDirectoryClient, self).__init__()
        self.__mode = "w+"
        self.__available_modes = modes - {self.__mode}
        self.__files = []

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        self.__directory = directory
        self.extend(iterable)

    def __repr__(self):
        return "PersistentDirectoryClient(%s)" % self.__str__()

    def __str__(self):
        s = ", ".join(map(repr, self))
        return "[%s]" % s

    def __del__(self):
        for f in self.__files:
            f.close()

    def __delitem__(self, index):
        """Delete item from given index.

        Delete means here:
        - delete file under `files[index]`
        - when item is deleted then list become smaller
        - rename and reopen higher than index files
        """
        file = self.__files[index]
        del self.__files[index]
        os.remove(file.name)

        for i in range(len(self.__files))[::-1]:
            if i < index:
                continue

            self.__files[i].close()
            old_file_path = self.get_file_path(i + 1)
            new_file_path = self.get_file_path(i)
            os.rename(old_file_path, new_file_path)

        for i in range(len(self.__files)):
            if i < index:
                continue

            file_path = self.get_file_path(i)
            file.seek(0)
            file = open(file_path, mode="r+")
            self.__files[i] = file

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            start, stop, step = indices
            items = (self[i] for i in range(start, stop, step))
            return self.__class__(
                self.__directory,
                iterable=items,
            )

        file = self.__files[index]
        file.seek(0)
        return file.read()

    def __setitem__(self, index, value):
        file_path = self.get_file_path(index)
        file = self.safe_write(file_path, value)
        self.__files[index] = file

    def __len__(self):
        return len(self.__files)

    def get_file_path(self, index):
        return f"{self.__directory}/{index}"

    def insert(self, index, value):
        """Insert value to index.

        Messy function. Two possible scenarios:
        1. Index is bigger than list - put value to end of a list

        2. Index is in the list and need to move a values.
           In this scenario:
           - close files that are higher than index (files[i] > index)
           - closed files rename and give higher number so file `4` becomes `5`
           - create new file, put value, put in the list `files`
           - reopen again files above index
        """
        if index >= len(self.__files):
            file_path = self.get_file_path(index)
            file = self.safe_write(file_path, value)
            self.__files.insert(index, file)
            return

        for i in range(len(self.__files))[::-1]:
            if i < index:
                continue

            self.__files[i].close()
            old_file_path = self.get_file_path(i)
            new_file_path = self.get_file_path(i + 1)
            os.rename(old_file_path, new_file_path)

        file_path = self.get_file_path(index)
        file = self.safe_write(file_path, value)
        self.__files.insert(index, file)

        for i in range(len(self.__files)):
            if i <= index:
                continue

            file_path = self.get_file_path(i)
            file.seek(0)
            file = open(file_path, mode="r+")

            self.__files[i] = file

    def __write(self, file_path, value, mode: Optional[str] = None):
        mode = mode or self.__mode
        file = open(file_path, mode=mode)
        file.write(value)
        file.seek(0)
        return file

    def safe_write(self, file_path, value):
        try:
            return self.__write(file_path, value)
        except TypeError:
            pass

        exc = None

        for mode in self.__available_modes:
            try:
                return self.__write(file_path, value, mode=mode)
            except TypeError as e:
                exc = e

        raise exc