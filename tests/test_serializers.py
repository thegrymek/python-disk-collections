def test_encode_decode(primitive_value, serializer_class):
    encoded = serializer_class.dumps(primitive_value)
    decoded = serializer_class.loads(encoded)
    assert primitive_value == decoded
