import json
import pickle
import zlib

from diskcollections.interfaces import ISerializer


class PickleSerializer(ISerializer):
    dumps = staticmethod(pickle.dumps)
    loads = staticmethod(pickle.loads)


class PickleZLibSerializer(ISerializer):
    @staticmethod
    def dumps(
        obj, protocol=pickle.HIGHEST_PROTOCOL, level=zlib.Z_DEFAULT_COMPRESSION
    ):
        pickled = pickle.dumps(obj, protocol=protocol)
        compressed = zlib.compress(pickled, level)
        return compressed

    @staticmethod
    def loads(compressed):
        pickled = zlib.decompress(compressed)
        obj = pickle.loads(pickled)
        return obj


class JsonSerializer(ISerializer):
    dumps = staticmethod(json.dumps)
    loads = staticmethod(json.loads)


class JsonZLibSerializer(ISerializer):
    @staticmethod
    def dumps(obj, level=zlib.Z_DEFAULT_COMPRESSION):
        jsoned = json.dumps(obj).encode()
        compressed = zlib.compress(jsoned, level)
        return compressed

    @staticmethod
    def loads(compressed):
        jsoned = zlib.decompress(compressed).decode()
        obj = json.loads(jsoned)
        return obj
