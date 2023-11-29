=======================
Python Disk Collections
=======================

.. image:: https://img.shields.io/pypi/v/python-disk-collections.svg
  :target: https://pypi.python.org/pypi/python-disk-collections

.. image:: https://img.shields.io/pypi/l/python-disk-collections.svg
  :target: https://pypi.python.org/pypi/python-disk-collections

.. image:: https://img.shields.io/pypi/pyversions/python-disk-collections.svg
  :target: https://pypi.python.org/pypi/python-disk-collections

.. image:: https://travis-ci.org/thegrymek/python-disk-collections.svg?branch=master
  :target: https://travis-ci.org/thegrymek/python-disk-collections

.. image:: https://coveralls.io/repos/github/thegrymek/python-disk-collections/badge.svg
  :target: https://coveralls.io/github/thegrymek/python-disk-collections


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

    >>> from diskcollections.iterables import FileList, FileDeque
    >>> from diskcollections.serializers import (
        PickleSerializer,  # pickle items
        PickleZLibSerializer,  # pickle + compress items
        JsonSerializer, # convert to json items
        JsonZLibSerializer  # convert to json + compress items
    )
    >>> from functools import partial
    >>> JsonFileList = partial(FileList, serializer_class=JsonHandler)
    >>> flist = JsonFileList()
    >>> flist.append({'a': 1, 'b': 2, 'c': 3})
    >>> flist[0]
    {u'a': 1, u'b': 2, u'c': 3}


Installation
------------

To install package type

.. code-block:: bash

    $ pip install python-disk-collections


How it works
------------

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


Contribute
----------

#. Fork repository on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write tests that prove that bug or future works as expected
#. Install other python versions with **pyenv** together with **tox**:

.. code-block:: bash

  $ sudo apt-get install pyenv tox

#. Install other python versions

.. code-block:: bash

  $ pyenv install 2.7 3.5 3.6 3.7 3.8 3.9 3.10 3.11


#. Make them global for **detox** package

.. code-block:: bash

  $ pyenv global 2.7 3.5 3.6 3.7 3.8 3.9 3.10 3.11

#. Install globally **detox**

.. code-block:: bash

  $ sudo pip install detox

#. Check your code and tests with **detox**

.. code-block:: bash

  $ detox -n 1
  GLOB sdist-make: python-disk-collections/setup.py
  lint inst-nodeps: python-disk-collections/.tox/.tmp/package/7/python-disk-collections-0.0.4.zip
  lint run-test-pre: PYTHONHASHSEED='1334400931'
  lint runtests: commands[0] | flake8
  lint runtests: commands[1] | python setup.py check -r -s -m
  py27 inst-nodeps: python-disk-collections/.tox/.tmp/package/7/python-disk-collections-0.0.4.zip
  py27 run-test-pre: PYTHONHASHSEED='1334400931'
  py27 runtests: commands[0] | py.test -v --cov diskcollections --cov-config .coveragerc --cov-report term-missing --cov-fail-under 95
  ...
  py311 inst-nodeps: python-disk-collections/.tox/.tmp/package/7/python-disk-collections-0.0.4.zip
  py311 run-test-pre: PYTHONHASHSEED='1334400931'
  py311 runtests: commands[0] | py.test -v --cov diskcollections --cov-config .coveragerc --cov-report term-missing --cov-fail-under 95
  _________________________________________________________________________________________________________________ summary __________________________________________________________________________________________________________________
    lint: commands succeeded
    py27: commands succeeded
    py35: commands succeeded
    py36: commands succeeded
    py37: commands succeeded
    py38: commands succeeded
    py39: commands succeeded
    py310: commands succeeded
    py311: commands succeeded
    congratulations :)

#. Send a pull request!


License
-------

Python-Disk-Collection is under MIT license, see LICENSE for more details.
