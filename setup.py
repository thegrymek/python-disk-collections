from setuptools import (
    find_packages,
    setup,
)


def url(*args):
    return '/'.join(args)


package_name = 'diskcollections'
url_profile = 'https://github.com/thegrymek'
setup(
    name=package_name,
    version='0.0.1',
    author='thegrymek',
    author_email='andrzej.grymkowski@gmail.com',
    description='Package provides class FileList that behaves like bulltin '
                'list but keeps your items at disk.',
    packages=find_packages(),
    tests_require=['pytest', 'tox', 'flake8'],
    url=url(url_profile, package_name),
    download_url=url(url_profile, package_name, '/archive/0.0.1.tar.gz'),
    license='MIT',
    zip_safe=False,
    keywords=['pickle', 'cache', 'collections', 'list', 'json', 'zlib'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
