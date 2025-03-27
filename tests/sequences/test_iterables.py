import collections
from copy import copy

import pytest

from diskcollections.iterables import Deque, FileDeque, FileList, List


class TestFileList:
    def test_init(self):
        l1 = FileList([1, "a", [5, "b"]])
        assert len(l1) == 3
        assert l1[0] == 1
        assert l1[1] == "a"
        assert l1[2] == [5, "b"]

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

    def test_copy(self):
        l1 = FileList([1, 2, 2, 3, 3, 3])
        l2 = copy(l1)
        assert l1 == l2
        assert l1 is not l2
        assert isinstance(l2, List)

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
        l1 = [1, "b", ["abc", 3], {1, 2, 3}]
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


class TestFileDeque:
    def test_init(self):
        d1 = FileDeque([1, "a", [5, "b"]])
        assert len(d1) == 3
        assert d1 == [1, "a", [5, "b"]]

    def test_maxlen(self):
        d1 = FileDeque([1, 2], maxlen=3)
        assert d1 == [1, 2]

        d1.extend([4, 4])
        assert d1 == [2, 4, 4]

        d1.appendleft(1)
        assert d1 == [1, 2, 4]

    def test_append(self):
        d1 = FileDeque()
        d1.append(1)
        assert d1.pop() == 1

        d1.append(2)
        d1.appendleft(1)
        assert d1.popleft() == 1
        assert d1.pop() == 2

    def test_pop(self):
        d1 = FileDeque([1, 2, 3])
        assert d1.popleft() == 1
        assert d1.popleft() == 2
        assert d1.popleft() == 3

    def test_pop_iterable(self):
        d1 = FileDeque(range(10))
        for _ in range(10):
            d1.popleft()

        assert not len(d1)

        d1.extend(range(100))

        for _ in range(10):
            d1.popleft()

        assert len(d1) == 90
        assert d1 == list(range(10, 100))

    def test_pop_exceptions(self):
        with pytest.raises(IndexError):
            FileDeque().pop()

        with pytest.raises(IndexError):
            FileDeque().popleft()

        with pytest.raises(IndexError):
            d1 = FileDeque([1, 2, 3])
            for _ in range(4):
                d1.pop()

    def test_extend(self):
        d1 = FileDeque()
        d1.extend([3, 4, 5])
        d1.extendleft([2, 1, 0])
        assert d1 == [0, 1, 2, 3, 4, 5]

    def test_iterable(self):
        test_list = [1, 2, 3, 4]
        d1 = FileDeque(test_list)

        for expected, i in zip(d1, test_list):
            assert expected == i

    def test_clear(self):
        d1 = FileDeque([1, 2, 3])
        assert d1 == [1, 2, 3]

        d1.clear()
        assert d1 == []

    def test_clear_exception(self):
        d1 = FileDeque()
        with pytest.raises(IndexError):
            d1.pop()

    def test_rotate(self):
        tested = range(10)
        d1 = FileDeque(tested)
        d2 = collections.deque(tested)

        d1.rotate(1)
        d2.rotate(1)
        assert d1 == d2

        d1.rotate(-2)
        d2.rotate(-2)
        assert d1 == d2

        d1.rotate(11)
        d2.rotate(11)
        assert d1 == d2

        d1.rotate(-11)
        d2.rotate(-11)
        assert d1 == d2

        d1.rotate(-6)
        d2.rotate(-6)
        assert d1 == d2

    def test_rotate_one_elem(self):
        d1 = FileDeque([1])
        d1.rotate(3)
        assert d1 == [1]

    def test_getitem(self):
        given = [1, 2, 3]
        d1 = FileDeque(given)
        for i, x in enumerate(given):
            assert d1[i] == x

    def test_insert(self):
        d1 = FileDeque()

        d1.insert(5, "c")
        assert d1[0] == "c"

        d1.insert(0, "a")
        d1.insert(1, "b")
        assert d1[0] == "a"
        assert d1[1] == "b"

    def test_count(self):
        d1 = FileDeque([1, 2, 2, 3, 3, 3])
        assert d1.count(1) == 1
        assert d1.count(2) == 2
        assert d1.count(3) == 3

    def test_str(self):
        l1 = [1, "b", ["abc", 3], {1, 2, 3}]
        d1 = FileDeque(l1)
        assert str(l1) == str(d1)

    def test_copy(self):
        d1 = FileDeque([1, 2, 2, 3, 3, 3])
        d2 = copy(d1)
        assert d1 == d2
        assert d1 is not d2
        assert isinstance(d2, Deque)

    def test_eq(self):
        d1 = FileDeque([1, 2, 3])
        assert not d1 == [1, 2]
        assert not d1 == [1, 2, 3, 4]
        assert not d1 == [3, 2, 1]
        assert d1 == [1, 2, 3]

    def test_neq(self):
        d1 = FileDeque([1, 2, 3])
        assert d1 != [1, 2]
        assert d1 != [1, 2, 3, 4]
        assert d1 != [3, 2, 1]
        assert not d1 != [1, 2, 3]

    def test_lt(self):
        d1 = FileDeque([1, 2, 3])
        assert d1 < [2, 3, 4, 5]
        assert d1 < [2, 3, 5]
        assert not d1 < [0]
        assert not d1 < [1, 2, 3]

    def test_le(self):
        d1 = FileDeque([1, 2, 3])
        assert d1 <= [2, 3, 4, 5]
        assert d1 <= [2, 3, 5]
        assert d1 <= [1, 2, 3]
        assert not d1 <= [0, 1, 2]

    def test_gt(self):
        d1 = FileDeque([1, 2, 3])
        assert d1 > [0, 1, 2]
        assert d1 > [0, 1, 2, 3]
        assert d1 > []
        assert not d1 > [2, 3, 4]

    def test_ge(self):
        d1 = FileDeque([1, 2, 3])
        assert d1 >= [0, 1, 2]
        assert d1 >= [1, 2, 3]
        assert d1 >= [0, 1, 2, 3]
        assert d1 >= []
        assert not d1 >= [2, 3, 4]

    def test_iadd(self):
        d1 = FileDeque([1, 2, 3])
        d1 += [4, 5, 6]
        assert d1 == [1, 2, 3, 4, 5, 6]
