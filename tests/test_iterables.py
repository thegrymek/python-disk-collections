import pytest
from diskcollections.iterables import FileList


class TestFileList:

    def test_init(self):
        l1 = FileList([1, 'a', [5, 'b']])
        assert len(l1) == 3
        assert l1[0] == 1
        assert l1[1] == 'a'
        assert l1[2] == [5, 'b']

    def test_init_exceptions(self):
        with pytest.raises(TypeError):
            FileList(*[1, 2, 3])

        with pytest.raises(TypeError):
            FileList(1, 2, 3)

    def test_get(self):
        l1 = FileList([0, 1, 2])
        assert l1[-3] == 0
        assert l1[-2] == 1
        assert l1[-1] == 2
        assert l1[0] == 0
        assert l1[1] == 1
        assert l1[2] == 2

    def test_set(self):
        l1 = FileList([0, 1, 2])
        l1[0] = 2
        l1[-1] = 0
        assert l1[0] == 2
        assert l1[2] == 0
        assert l1 == [2, 1, 0]

    def test_append(self):
        l1 = FileList()
        l1.append(1)
        assert l1[0] == 1

    def test_extend(self):
        l1 = FileList([0, 1, 2])
        l2 = FileList([4, 5, 6])

        l1.extend(l2)
        assert l1[3] == 4
        assert l1[4] == 5
        assert l1[5] == 6

        for i in l2:
            assert i in l1

    def test_del(self):
        l1 = FileList([0, 1, 2])
        assert l1[1] == 1

        del l1[1]
        assert len(l1) == 2
        assert l1[1] == 2

    def test_iter(self):
        l1 = FileList([0, 1, 2])
        check_list = [0, 1, 2]

        for n, i in enumerate(l1):
            assert i == check_list[n]

    def test_index_error(self):
        l1 = FileList()
        with pytest.raises(IndexError):
            a = l1[0]
            print(a)

    def test_equal(self):
        l1 = FileList([1, 2, 3, 4])
        assert l1 == [1, 2, 3, 4]
        assert not l1 == [1, 3, 4, 2]
        assert not l1 == [1, 2, 3, 4, 5]
        assert not l1 == [2, 3, 4]

    def test_convert(self):
        l1 = FileList([1, 2, 3, 4])
        assert l1 == [i for i in l1]
        assert l1 == list(l1)
        assert l1 == l1[:]
        assert l1[:2] == l1[:2]
        assert l1[2:] == l1[2:]
        assert l1[2:3] == l1[2:3]

    def test_str(self):
        l1 = [1, 'b', ['abc', 3], {1, 2, 3}]
        f1 = FileList(l1)
        assert str(l1) == str(f1)

    def test_insert(self):
        l1 = FileList([1])
        l1.insert(0, 0)
        assert l1[0] == 0
        assert l1[1] == 1

    def test_overlaps_insert(self):
        l1 = FileList()
        l1.insert(0, 2)
        l1.insert(0, 1)
        l1.insert(0, 0)
        assert l1 == [0, 1, 2]

        l1.insert(1, 5)
        l1.insert(2, 6)
        l1.insert(4, 7)
        assert l1 == [0, 5, 6, 1, 7, 2]

        l1[0] = 10
        l1[2] = 20
        l1[4] = 30
        assert l1 == [10, 5, 20, 1, 30, 2]
