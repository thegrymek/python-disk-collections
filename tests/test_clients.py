import pytest
from diskcollections import clients


class TestTemporaryFileClient:

    @property
    def key(self):
        return 'a'

    @property
    def value(self):
        return 'abc'

    def test_get_store(self):
        client = clients.TemporaryFileClient()
        client.set(self.key, self.value)
        assert client.get(self.key) == self.value

    def test_exceptions(self):
        client = clients.TemporaryFileClient()

        with pytest.raises(KeyError):
            client.get(self.value)

        with pytest.raises(KeyError):
            client.delete(self.value)

    def test_set_bytes(self):
        client = clients.TemporaryFileClient()
        bytes_value = 'abc'.encode()

        client.set(self.key, bytes_value)
        assert client.get(self.key) == bytes_value

    def test_multiple_clients(self):
        """Check if clients do not overlaps."""
        many_clients = [
            clients.TemporaryFileClient()
            for _ in range(100)
        ]
        for i, client in enumerate(many_clients):
            client.set(self.key, self.value + str(i))

        for i, client in enumerate(many_clients):
            assert client.get(self.key) == self.value + str(i)
