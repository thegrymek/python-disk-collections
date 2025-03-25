import os
from setuptools import (
    find_packages,
    setup,
)


def url(*args):
    return '/'.join(args)


here = os.path.abspath(os.path.dirname(__file__))
with open('README.rst', 'r') as f:
    readme = f.read()

package_name = 'python-disk-collections'
url_profile = 'https://github.com/thegrymek'
version = '0.0.5'
setup(
    name=package_name,
    version=version,
    author='thegrymek',
    author_email='andrzej.grymkowski@gmail.com',
    description='Package provides classes: FileList, FileDeque that behaves '
                'like bulltins but keeps items at disk.',
    long_description=readme,
    packages=find_packages(),
    url=url(url_profile, package_name),
    download_url=url(url_profile, package_name, 'archive/%s.tar.gz' % version),
    license='MIT',
    zip_safe=False,
    keywords=['pickle', 'cache', 'collections', 'list', 'deque', 'json',
              'zlib', 'disk'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
