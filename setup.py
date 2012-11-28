#!/usr/bin/env python

"""
distutils/setuptools install script. See inline comments for packaging documentation.
"""

from distutils.core import setup
from remotely import __version__ as version
import os
import sys

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

#version = "0.2.0"

print version

setup(
    name = "remotely",
    version = version,
    packages = ["remotely"],
    author = "Kefei Dan Zhou",
    author_email = "kefei.zhou@gmail.com",
    url = "http://pypi.python.org/pypi/remotely",
    download_url = "http://pypi.python.org/packages/source/r/remotely/remotely-%s.tar.gz" % (version,),
    license = "http://www.opensource.org/licenses/bsd-3-clause",
    description = "Remotely is a simple and secure remote code execution api",
    long_description=open('README.rst').read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Distributed Computing',
        'Topic :: Utilities',
    ],
)

