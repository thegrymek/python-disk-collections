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


class IClient:
    """Abstract client to get, set, delete items."""

    def set(self, key, content):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
