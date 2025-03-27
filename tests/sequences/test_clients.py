import os.path

from diskcollections.iterables import clients


class TestTemporaryDirectoryClient:
    def create_client(self, mode="w+"):
        return clients.TemporaryDirectoryClient(mode=mode)

    def test_append(self):
        client = self.create_client()
        client.append("abc")
        assert client[0] == "abc"

    def test_insert(self):
        client = self.create_client()
        client.extend(["a", "b", "c"])
        client.insert(1, "z")
        assert list(client) == ["a", "z", "b", "c"]

    def test_slice(self):
        client = self.create_client()
        client.extend(["a", "b", "c"])
        assert list(client[0:2]) == ["a", "b"]


class TestPersistentDirectoryClient:
    def create_client(self):
        return clients.PersistentDirectoryClient("persistent_dir")

    def test_append(self):
        client = self.create_client()
        client.append("abc")
        assert client[0] == "abc"

    def test_insert(self):
        client = self.create_client()
        client.extend(["a", "b", "c", "d"])
        client.insert(1, "z")
        assert list(client) == ["a", "z", "b", "c", "d"]

        client[2] = "x"
        assert list(client) == ["a", "z", "x", "c", "d"]

        del client[3]
        assert list(client) == ["a", "z", "x", "d"]

        client.append("y")

        assert list(client) == ["a", "z", "x", "d", "y"]

    def test_slice(self):
        client = self.create_client()
        client.extend(["a", "b", "c"])
        assert list(client[0:2]) == ["a", "b"]

    def test_dir_exists(self):
        client = self.create_client()
        assert os.path.exists("persistent_dir")

        # clean up
        del client
        # directory should still exist
        assert os.path.exists("persistent_dir")

    def test_remove(self):
        client = self.create_client()
        client.append("0")
        assert list(client) == ["0"]
        assert os.path.exists("persistent_dir/0")

        # explicitly remove will delete file
        del client[0]
        assert list(client) == []
        assert not os.path.exists("persistent_dir/0")
