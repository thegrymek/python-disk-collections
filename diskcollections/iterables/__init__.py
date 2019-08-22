from functools import partial

from ..serializers import (
    PickleZLibSerializer
)
from .clients import (
    TemporaryDirectoryClient
)
from .iterables import (
    Deque,
    List
)


FileList = partial(
    List,
    client_class=TemporaryDirectoryClient,
    serializer_class=PickleZLibSerializer
)

FileDeque = partial(
    Deque,
    client_class=TemporaryDirectoryClient,
    serializer_class=PickleZLibSerializer
)

__all__ = (
    'List', 'Deque',
    'FileDeque', 'FileList', 'TemporaryDirectoryClient'
)
