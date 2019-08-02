import pytest
from diskcollections import serializers

primitive_values = [
    'a',
    1,
    [1, 2, 3],
    {'a': 1, 'b': 2, 'c': [1, 2, 3]}
]

serializers_classes = [
    serializers.JsonSerializer,
    serializers.JsonZLibSerializer,
    serializers.PickleSerializer,
    serializers.PickleZLibSerializer,
]


@pytest.fixture(
    params=primitive_values,
    ids=list(map(str, primitive_values))
)
def primitive_value(request):
    return request.param


@pytest.fixture(
    params=serializers_classes,
    ids=list(map(str, serializers_classes))
)
def serializer_class(request):
    return request.param


def test_encode_decode(primitive_value, serializer_class):
    encoded = serializer_class.dumps(primitive_value)
    decoded = serializer_class.loads(encoded)
    assert primitive_value == decoded
