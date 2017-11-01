=======================
Python Disk Collections
=======================

.. image:: https://travis-ci.org/thegrymek/python-disk-collections.svg?branch=master
  :target: https://travis-ci.org/thegrymek/python-disk-collections

.. image:: https://coveralls.io/repos/github/thegrymek/python-disk-collections/badge.svg
  :target: https://coveralls.io/github/thegrymek/python-disk-collections


Module contains class with extended python list that stores items at disk.
By default items before save are pickled and compressed. Use that list
as usual list!

Intend of package was to create generic list that stores really big list of items
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


There are available more ways to serialize items.


.. code-block:: python

    >>> from diskcollections.iterables import FileList
    >>> from diskcollections.handlers import (
        PickleHandler,  # pickle items
        PickleZLibHandler,  # pickle + compress items
        JsonHandler, # convert to json items
        JsonZLibHandler  # convert to json + compress items
    )
    >>> from functools import partial
    >>> JsonFileList = partial(FileList, handler_class=JsonHandler)
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

    >>> from diskcollections.interfaces import IHandler

    class IHandler:

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

All handlers from example above implements interface **IHandler**.

Under the hood, **FileList** for storage items uses *tempfile.mktemp* (in python2)
or *tempfile.TemporaryDirectory* (in python3). It means, that every list
has own unique directory, placed likely in */tmp/*.
When list is removed by garbage collector, all items that was stored are lost.


Contribute
----------

#. Fork `repository https://github.com/thegrymek/python-disk-collections.git`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write tests that prove that bug or future works as expected
#. Check your code and tests with **tox**
#. Send a pull request!


License
-------

Python-Disk-Collection is under MIT license, see LICENSE for more details.
