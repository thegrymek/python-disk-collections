from diskcollections.iterables import FileDeque, FileList, List, Deque


def test_file_list() -> None:
    flist = FileList()
    flist.extend([1, 2, 3])
    flist.append(4)
    assert all(i in flist for i in [1, 2, 3, 4])

    flist2 = flist[:]
    assert isinstance(flist2, List)

    my_list = list(flist)
    assert isinstance(my_list, list)


def test_file_deque() -> None:
    fdeque = FileDeque()
    fdeque.extend([1, 2, 3])
    fdeque.append(4)
    assert all(i in fdeque for i in [1, 2, 3, 4])

    fdeque = FileDeque([1, 2, 3, 4])
    assert fdeque.pop() == 4
    fdeque.appendleft(0)
    assert fdeque.popleft() == 0


def test_list_serializers(client_class, serializer_class) -> None:
    expected = [{"a": 1, "b": 2, "c": 3}, "a", 1]
    flist = List(client_class=client_class, serializer_class=serializer_class)
    flist.extend(expected)
    assert all(i in flist for i in expected)
    assert flist == expected
    assert list(flist) == expected


def test_deque_serializers(client_class, serializer_class) -> None:
    expected = [{"a": 1, "b": 2, "c": 3}, "a", 1]
    fdeque = Deque(
        client_class=client_class, serializer_class=serializer_class
    )
    fdeque.extend(expected)
    assert all(i in fdeque for i in expected)
    assert fdeque == expected
    assert list(fdeque) == expected
