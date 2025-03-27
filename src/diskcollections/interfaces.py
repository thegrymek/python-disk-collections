import collections


class ISerializer:
    @staticmethod
    def dumps(obj):
        """Converts object to serialized format.

        :param obj: any python object
        :return: serialized object
        """
        raise NotImplementedError

    @staticmethod
    def loads(obj):
        """Restored dumped string into python object.

        :param obj: Serialized object
        :return: restored python object
        """
        raise NotImplementedError


class IClientSequence(collections.abc.MutableSequence):
    """Abstract client to manage items in sequence.

    Inheritance class has to implement following methods:
    * `__getitem__(index)`
    * `__setitem__(index, value)`
    * `__delitem__(index)`
    * ` __len__()`
    * `insert(item)`
    """
