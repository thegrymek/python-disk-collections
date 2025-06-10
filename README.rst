=======================
Python Disk Collections
=======================

.. image:: https://img.shields.io/pypi/v/python-disk-collections.svg
  :target: https://pypi.python.org/pypi/python-disk-collections

.. image:: https://img.shields.io/pypi/l/python-disk-collections.svg
  :target: https://pypi.python.org/pypi/python-disk-collections

.. image:: https://img.shields.io/pypi/pyversions/python-disk-collections.svg
  :target: https://pypi.python.org/pypi/python-disk-collections

.. image:: https://img.shields.io/pypi/dm/python-disk-collections
  :target: https://pypi.python.org/pypi/python-disk-collections


Module contains class with extended python list that stores items at disk.
By default items before save are pickled and compressed. Use that list
as usual list!

In addition, there is implemented extended python deque with disk storage and
same behaviour as **collections.deque**.

Intend of package was to create generic iterables that stores really big collection of items
that does not fit in memory and to avoid usage of external cache and local database
storages.


.. code-block:: python

    >>> from diskcollections.iterables import FileList
    >>> flist = FileList()
    >>> flist.extend([1, 2, 3])
    >>> flist.append(4)
    >>> flist
    [1, 2, 3, 4]
    >>> flist[2]
    3
    >>> flist2 = flist[:]  # copy makes new FileList
    >>> my_list = list(flist)  # now its simple list


.. code-block:: python

    >>> from diskcollections.iterables import FileDeque
    >>> fdeque = FileDeque()
    >>> fdeque.extend([1, 2, 3])
    >>> fdeque.append(4)
    >>> fdeque
    FileDeque([1, 2, 3, 4])
    >>> fdeque.pop()
    4
    >>> fdeque.appendleft(0)
    >>> fdeque.popleft()
    0


There are available more ways to serialize items.


.. code-block:: python

    >>> from diskcollections.iterables import List, FileList, FileDeque
    >>> from diskcollections.serializers import (
        PickleSerializer,  # pickle items
        PickleZLibSerializer,  # pickle + compress items
        JsonSerializer, # convert to json items
        JsonZLibSerializer  # convert to json + compress items
    )
    >>> from functools import partial
    >>> JsonFileList = partial(FileList, serializer_class=JsonSerializer)
    >>> flist = JsonFileList()
    >>> flist.append({'a': 1, 'b': 2, 'c': 3})
    >>> flist[0]
    {'a': 1, 'b': 2, 'c': 3}


Installation
------------

To install package type

.. code-block:: bash

    $ pip install python-disk-collections


How it works
------------

Explaining example above:

.. code-block:: python

    >>> from diskcollections.iterables import FileList
    >>> from diskcollections.serializers import JsonZLibSerializer
    >>>
    >>> flist = FileList(serializer_class=JsonZLibSerializer)

New instance of this object creates new temporary directory.
By using `serializer_class=JsonZLibSerializer` each incoming item to list will be: json.dumped and compressed

.. code-block:: python

    >>> flist.append({'a': 1, 'b': 2, 'c': 3})

so using this serializer have in mind that all objects you put into list
have to lend themself and compatible with json.
Exactly this object `{'a': 1, 'b': 2, 'c': 3}` will serialized and compressed and saved inside temporary directory.

.. code-block:: python

    >>> flist[0]
    {'a': 1, 'b': 2, 'c': 3}

Getting an item will read a file and because `JsonZLibSerializer` is used: then content will be decompressed and tried
to loaded from json.

This package provides a few other serializers:

* PickleSerializer - pickle items
* PickleZLibSerializer - pickle + compress items
* JsonSerializer - convert to json items
* JsonZLibSerializer - convert to json + compress items

.. code-block:: python

    from diskcollections.serializers import (
          PickleSerializer,
          PickleZLibSerializer,
          JsonSerializer,
          JsonZLibSerializer,
      )

In order to implement your serializer create class with methods:
**dumps** and **loads** or import interface.


.. code-block:: python

    >>> from diskcollections.interfaces import ISerializer

    class ISerializer:

    @staticmethod
    def dumps(obj):
        """Converts object to string.

        :param obj: any python object
        :return: dumped string
        """
        raise NotImplementedError

    @staticmethod
    def loads(obj):
        """Restored dumped string into python object.

        :param obj: Object stored as string
        :return: python object restored from dump
        """
        raise NotImplementedError

All serializers from example above implements interface **ISerializer**.

Under the hood, **FileList** for storage items uses *tempfile.mktemp* (in python2)
or *tempfile.TemporaryDirectory* (in python3). It means, that every list
has own unique directory, placed likely in */tmp/*.
When list is removed by garbage collector, all items that was stored are lost.

For **FileDeque** stores items in the same way as **FileList**.

By default on exit program, or when list or deque is removed: all content of files also are dropped.

To prevent this use `PersistentDirectoryClient`:

.. code-block:: python

    >>> from functools import partial

    >>> from diskcollections.iterables import List, PersistentDirectoryClient
    >>> from diskcollections.serializers import JsonSerializer
    >>> from diskcollections.iterables import PersistentDirectoryClient

    >>> dir_abc = partial(PersistentDirectoryClient, "abc")
    >>> persistent_list = List(client_class=dir_abc, serializer_class=JsonSerializer)
    >>> persistent_list.append({"a": 1, "b": 2})
    >>> assert len(persistent_list) == 1
    >>> assert open("abc/0").read() == '{"a": 1, "b": 2}'

On exit directory `abc` with file `0` of his contents will still exist.


Contribute
----------

#. Fork repository on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write tests that prove that bug or future works as expected
#. Install other python versions with **uv** together with **tox**:

.. code-block:: bash

  $ pip install uv
  $ uv sync
  $ uv tool install tox --with tox-uv

#. Install python versions

.. code-block:: bash

  $ uv python install 3.8 3.9 3.10 3.11 3.12 3.13

#. Check your code and tests with **tox**

.. code-block:: bash

  $ tox
  ---------- coverage: platform linux, python 3.13.2-final-0 -----------
  Name                                     Stmts   Miss Branch BrPart  Cover   Missing
  ------------------------------------------------------------------------------------
  diskcollections/__init__.py                  0      0      0      0   100%
  diskcollections/iterables/__init__.py        7      0      0      0   100%
  diskcollections/iterables/clients.py       112      1     28      1    99%   90
  diskcollections/iterables/iterables.py     159      0     74      0   100%
  diskcollections/serializers.py              32      0      0      0   100%
  ------------------------------------------------------------------------------------
  TOTAL                                      310      1    102      1    99%

  Required test coverage of 95% reached. Total coverage: 99.51%
  ====================================================================================================== 63 passed, 1 warning in 0.46s =======================================================================================================
    lint: OK (0.55=setup[0.03]+cmd[0.20,0.32] seconds)
    py37: OK (0.47=setup[0.01]+cmd[0.46] seconds)
    py38: OK (0.47=setup[0.01]+cmd[0.46] seconds)
    py39: OK (0.47=setup[0.01]+cmd[0.46] seconds)
    py310: OK (0.63=setup[0.01]+cmd[0.62] seconds)
    py311: OK (0.45=setup[0.01]+cmd[0.45] seconds)
    py312: OK (0.69=setup[0.01]+cmd[0.69] seconds)
    py313: OK (0.75=setup[0.01]+cmd[0.74] seconds)
    evaluation failed :( (4.12 seconds)

#. Lint your code

.. code-block:: bash

    $ tox -e lint

#. Send a pull request!


License
-------

Python-Disk-Collection is under MIT license, see LICENSE for more details.
