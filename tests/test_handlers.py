import pytest
from diskcollections import handlers

primitive_values = [
    'a',
    1,
    [1, 2, 3],
    {'a': 1, 'b': 2, 'c': [1, 2, 3]}
]

handlers_classes = [
    handlers.JsonHandler,
    handlers.JsonZLibHandler,
    handlers.PickleHandler,
    handlers.PickleZLibHandler,
]


@pytest.fixture(
    params=primitive_values,
    ids=list(map(str, primitive_values))
)
def primitive_value(request):
    return request.param


@pytest.fixture(
    params=handlers_classes,
    ids=list(map(str, handlers_classes))
)
def handler_class(request):
    return request.param


def test_encode_decode(primitive_value, handler_class):
    encoded = handler_class.dumps(primitive_value)
    decoded = handler_class.loads(encoded)
    assert primitive_value == decoded
