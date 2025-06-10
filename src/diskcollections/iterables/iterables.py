import collections
import inspect
from functools import partial
from diskcollections.py2to3 import izip


class List(collections.abc.MutableSequence):
    def __init__(
        self, iterable=None, client_class=None, serializer_class=None
    ):
        super(List, self).__init__()

        if inspect.isclass(client_class):
            self.__client = client_class()
        elif isinstance(client_class, partial):
            self.__client = client_class()
        else:
            self.__client = client_class

        self.__serializer = serializer_class

        iterable = iterable or []
        self.extend(iterable)

    def __repr__(self):
        return "%s%s" % (self.__class__, self.__str__())

    def __str__(self):
        s = ", ".join(map(repr, self))
        return "[%s]" % s

    def __copy__(self):
        return self.__class__(
            self,
            client_class=self.__client.__class__,
            serializer_class=self.__serializer,
        )

    def __eq__(self, other):
        total_items = len(self.__client)
        if total_items != len(other):
            return False

        for i, elem in enumerate(self):
            if elem != other[i]:
                return False
        return True

    def __delitem__(self, index):
        del self.__client[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            start, stop, step = indices
            return self.__class__(
                (self[i] for i in range(start, stop, step)),
                client_class=self.__client.__class__,
                serializer_class=self.__serializer,
            )
        encoded_value = self.__client[index]
        return self.__serializer.loads(encoded_value)

    def __setitem__(self, index, value):
        encoded_value = self.__serializer.dumps(value)
        self.__client[index] = encoded_value

    def __len__(self):
        return len(self.__client)

    def __del__(self):
        del self.__client

    def insert(self, index, value):
        encoded_value = self.__serializer.dumps(value)
        self.__client.insert(index, encoded_value)


class Deque(collections.abc.MutableSequence):
    def __init__(
        self,
        iterable=(),
        maxlen=None,
        client_class=None,
        serializer_class=None,
    ):
        if inspect.isclass(client_class):
            self.__client = client_class()
        elif isinstance(client_class, partial):
            self.__client = client_class()
        else:
            self.__client = client_class

        self.__serializer = serializer_class
        self.__max_length = maxlen
        self.extend(iterable)

    def __del__(self):
        del self.__client

    def __iter__(self):
        for idx in range(len(self)):
            yield self[idx]

    def __len__(self):
        return len(self.__client)

    def __repr__(self):
        return "%s(%s)" % (self.__class__, self.__str__())

    def __str__(self):
        s = ", ".join(map(repr, self))
        return "[%s]" % s

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

    #
    # mutable sequence
    #

    def __getitem__(self, idx):
        encoded_value = self.__client[idx]
        return self.__serializer.loads(encoded_value)

    def __setitem__(self, idx, value):
        encoded_value = self.__serializer.dumps(value)

        if idx >= len(self):
            self.__client.insert(idx, encoded_value)
        if idx < 0:
            self.__client.insert(0, encoded_value)

    def __delitem__(self, idx):
        del self.__client[idx]

    def insert(self, idx, value):
        encoded_value = self.__serializer.dumps(value)
        self.__client.insert(idx, encoded_value)

    #
    # deque methods
    #

    def append(self, x):
        self[len(self)] = x

        if self.__max_length and self.__max_length < len(self):
            self.popleft()

    def appendleft(self, x):
        self[-1] = x

        if self.__max_length and self.__max_length < len(self):
            self.pop()

    def extend(self, iterable):
        for x in iterable:
            self.append(x)

    def extendleft(self, iterable):
        for x in iterable:
            self.appendleft(x)

    def pop(self):
        if not len(self):
            raise IndexError("pop from an empty deque")

        last_idx = len(self) - 1
        value = self[last_idx]
        del self[last_idx]
        return value

    def popleft(self):
        if not len(self):
            raise IndexError("pop from an empty deque")

        value = self[0]
        del self[0]
        return value

    def clear(self):
        while len(self):
            self.popleft()

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
