import itertools
import shutil
import sys
import tempfile

if sys.version_info >= (3, 0):
    basestring = str
    izip = zip
else:
    basestring = basestring
    izip = itertools.izip

if sys.version_info >= (3, 4):
    TemporaryDirectory = tempfile.TemporaryDirectory
else:

    class TemporaryDirectory:
        def __init__(self):
            self._directory_path = tempfile.mkdtemp()

        @property
        def name(self):
            return self._directory_path

        def cleanup(self):
            shutil.rmtree(self.name)
