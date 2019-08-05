from diskcollections.iterables import clients


class TestTemporaryDirectoryClient:

    def create_client(self, mode='w+'):
        return clients.TemporaryDirectoryClient(mode=mode)

    def test_append(self):
        client = self.create_client()
        client.append('abc')
        assert client[0] == 'abc'

    def test_insert(self):
        client = self.create_client()
        client.extend(['a', 'b', 'c'])
        client.insert(1, 'z')
        assert list(client) == ['a', 'z', 'b', 'c']

    def test_slice(self):
        client = self.create_client()
        client.extend(['a', 'b', 'c'])
        assert list(client[0:2]) == ['a', 'b']
