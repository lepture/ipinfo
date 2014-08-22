#!/usr/bin/env python
# coding: utf-8


try:
    # python setup.py test
    import multiprocessing
except ImportError:
    pass

import ipinfo
from setuptools import setup


def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()

setup(
    name='ipinfo',
    version=ipinfo.__version__,
    url='https://github.com/lepture/ipinfo',
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    description='',
    long_description=fread('README.rst'),
    license='BSD',
    py_modules=['ipinfo'],
    zip_safe=False,
    platforms='any',
    tests_require=['nose'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing :: Markup',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
