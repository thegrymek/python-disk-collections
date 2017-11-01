import collections

from diskcollections import (
    clients,
    generators,
    handlers,
)


class FileList(collections.MutableSequence):

    def __init__(
        self,
        iterable=None,
        client_class=clients.TemporaryFileClient,
        handler_class=handlers.PickleZLibHandler,
        generator=generators.StringGenerator
    ):
        super(FileList, self).__init__()
        self.__storage = []
        self.__client = client_class()
        self.__handler = handler_class
        self.__generator = generator

        iterable = iterable or []
        self.extend(iterable)

    def __repr__(self):
        return 'FileList%s' % self.__str__()

    def __str__(self):
        s = ', '.join(map(repr, self))
        return '[%s]' % s

    def __eq__(self, other):
        total_items = len(self.__storage)
        if total_items != len(other):
            return False

        for i, elem in enumerate(self):
            if elem != other[i]:
                return False
        return True

    def __delitem__(self, index):
        key = self.__storage[index]
        del self.__storage[index]
        self.__client.delete(key)

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            start, stop, step = indices
            return self.__class__(
                self[i]
                for i in range(start, stop, step)
            )
        key = self.__storage[index]
        encoded_value = self.__client.get(key)
        return self.__handler.loads(encoded_value)

    def __setitem__(self, index, value):
        key = self.__storage[index]
        encoded_value = self.__handler.dumps(value)
        self.__client.set(key, encoded_value)

    def __len__(self):
        return len(self.__storage)

    def __del__(self):
        del self.__client
        del self.__storage
        self.__generator.delete(id(self))

    def insert(self, index, value):
        prefix = id(self)
        key = self.__generator.next(prefix)
        self.__storage.insert(index, key)
        self.__setitem__(index, value)
