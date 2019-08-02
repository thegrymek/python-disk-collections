import collections

from diskcollections import (
    clients,
    generators,
    serializers,
)
from diskcollections.py2to3 import izip


class FileList(collections.MutableSequence):

    def __init__(
        self,
        iterable=None,
        client_class=clients.TemporaryFileClient,
        serializer_class=serializers.PickleZLibSerializer,
        generator=generators.StringGenerator
    ):
        super(FileList, self).__init__()
        self.__storage = []
        self.__client = client_class()
        self.__serializer = serializer_class
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
        return self.__serializer.loads(encoded_value)

    def __setitem__(self, index, value):
        key = self.__storage[index]
        encoded_value = self.__serializer.dumps(value)
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


class FileDeque:

    def __init__(
        self,
        iterable=(),
        maxlen=None,
        client_class=clients.TemporaryFileClient,
        serializer_class=serializers.PickleZLibSerializer,
    ):
        self.__client = client_class()
        self.__serializer = serializer_class
        self.__left_index = 0
        self.__right_index = 0
        self.__length = 0
        self.__max_length = maxlen
        self.extend(iterable)

    def __del__(self):
        del self.__client

    def __iter__(self):
        for idx in range(self.__left_index, self.__right_index):
            yield self.__get(idx)

    def __len__(self):
        return self.__length

    def __repr__(self):
        return 'FileDeque(%s)' % self.__str__()

    def __str__(self):
        s = ', '.join(map(repr, self))
        return '[%s]' % s

    def __copy__(self):
        return self.__class__(
            self,
            maxlen=self.__max_length,
            client_class=self.__client.__class__,
            serializer_class=self.__serializer,
        )

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for i, j in izip(self, other):
            if i != j:
                return False

        return True

    def __ne__(self, other):
        if len(self) != len(other):
            return True

        for i, j in izip(self, other):
            if i != j:
                return True

        return False

    def __lt__(self, other):
        for i, j in izip(self, other):
            if i >= j:
                return False

        if len(self) >= len(other):
            return True

        return True

    def __le__(self, other):
        for i, j in izip(self, other):
            if i > j:
                return False

        if len(self) >= len(other):
            return True

        return True

    def __gt__(self, other):
        for i, j in izip(self, other):
            if i <= j:
                return False

        return True

    def __ge__(self, other):
        for i, j in izip(self, other):
            if i < j:
                return False

        return True

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __get(self, idx):
        encoded_value = self.__client.get(str(idx))
        return self.__serializer.loads(encoded_value)

    def __set(self, idx, value):
        encoded_value = self.__serializer.dumps(value)
        self.__client.set(str(idx), encoded_value)

    def __delete(self, idx):
        self.__client.delete(str(idx))

    def append(self, x):
        self.__set(self.__right_index, x)
        self.__right_index += 1
        self.__length += 1

        if self.__max_length and self.__max_length < self.__length:
            self.popleft()

    def appendleft(self, x):
        self.__length += 1
        if self.__max_length and self.__max_length < self.__length:
            self.pop()

        self.__left_index -= 1
        self.__set(self.__left_index, x)

    def extend(self, iterable):
        for x in iterable:
            self.append(x)

    def extendleft(self, iterable):
        for x in iterable:
            self.appendleft(x)

    def pop(self):
        if not self.__length:
            raise IndexError("pop from an empty deque")
        self.__right_index -= 1
        self.__length -= 1
        value = self.__get(self.__right_index)
        self.__delete(self.__right_index)
        return value

    def popleft(self):
        if not self.__length:
            raise IndexError("pop from an empty deque")
        value = self.__get(self.__left_index)
        self.__delete(self.__left_index)
        self.__left_index += 1
        self.__length -= 1
        return value

    def clear(self):
        for idx in range(self.__left_index, self.__right_index):
            self.__delete(idx)
        self.__left_index = 0
        self.__right_index = 0
        self.__length = 0

    def count(self, value):
        c = 0
        for item in self:
            if item == value:
                c += 1
        return c

    def rotate(self, n=1):
        """Rotates elements in deque.

        Its copy->paste from
        https://bitbucket.org/pypy/pypy/src/default/lib_pypy/_collections.py?fileviewer=file-view-default
        """
        length = len(self)
        if length <= 1:
            return
        halflen = length >> 1
        if n > halflen or n < -halflen:
            n %= length
            if n > halflen:
                n -= length
        while n > 0:
            self.appendleft(self.pop())
            n -= 1
        while n < 0:
            self.append(self.popleft())
            n += 1
