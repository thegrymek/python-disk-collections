import shutil
import uuid
from functools import partial

import pathlib
import pytest

from diskcollections import serializers
from diskcollections.iterables import clients, List

from diskcollections.iterables import FileDeque

here = pathlib.Path(__file__).parent.absolute()
test_persistent_dir = here / "persistent_dir"


primitive_values = ["a", 1, [1, 2, 3], {"a": 1, "b": 2, "c": [1, 2, 3]}]


@pytest.fixture(params=primitive_values, ids=list(map(str, primitive_values)))
def primitive_value(request):
    return request.param


serializers_classes = [
    serializers.JsonSerializer,
    serializers.JsonZLibSerializer,
    serializers.PickleSerializer,
    serializers.PickleZLibSerializer,
]


@pytest.fixture(
    params=serializers_classes, ids=list(map(str, serializers_classes))
)
def serializer_class(request):
    return request.param


@pytest.fixture(
    params=[
        clients.TemporaryDirectoryClient,
        partial(
            clients.PersistentDirectoryClient,
            test_persistent_dir / str(uuid.uuid4()),
        ),
    ],
    ids=["TemporaryDirectoryClient", "PersistentDirectoryClient"],
)
def client_class(request):
    test_persistent_dir.mkdir(exist_ok=True)
    yield request.param
    shutil.rmtree(test_persistent_dir.absolute())


@pytest.fixture(
    params=[
        partial(
            List,
            client_class=partial(clients.TemporaryDirectoryClient, mode="w+b"),
            serializer_class=serializers.PickleZLibSerializer,
        )
    ],
    ids=["FileList"],
)
def list_class(request):
    return request.param


@pytest.fixture(params=[FileDeque], ids=["FileDeque"])
def deque_class(request):
    return request.param
