import tempfile

from diskcollections.interfaces import IClientSequence
from diskcollections.py2to3 import TemporaryDirectory


class TemporaryDirectoryClient(IClientSequence):
    """
    Client that stores every item in separated file in temporary directory.

    When client is removed, all files and directory are also removed.
    Client creates new file on every new item.
    If under index file exist, then file will be removed and created with
    new content.
    """

    def __init__(self, iterable=(), mode='w+b'):
        super(TemporaryDirectoryClient, self).__init__()
        self.__mode = mode
        self.__files = []
        self.__directory = TemporaryDirectory()
        self.extend(iterable)

    def __repr__(self):
        return 'TemporaryDirectoryClient(%s)' % self.__str__()

    def __str__(self):
        s = ', '.join(map(repr, self))
        return '[%s]' % s

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
            items = (
                self[i]
                for i in range(start, stop, step)
            )
            return self.__class__(items, mode=self.__mode)

        file = self.__files[index]
        file.seek(0)
        return file.read()

    def __setitem__(self, index, value):
        file = tempfile.TemporaryFile(
            mode=self.__mode,
            dir=self.__directory.name
        )
        file.write(bytes(value))
        self.__files[index] = file

    def __len__(self):
        return len(self.__files)

    def insert(self, index, value):
        file = tempfile.TemporaryFile(
            mode=self.__mode,
            dir=self.__directory.name
        )
        file.write(value)
        self.__files.insert(index, file)
