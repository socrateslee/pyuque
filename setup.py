#!/usr/bin/env python
from pyuque import __VERSION__

long_description = ""

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    pass

sdict = {
    'name': 'pyuque',
    'version': __VERSION__,
    'packages': ['pyuque',
                 'pyuque.util'],
    'zip_safe': False,
    'install_requires': ['requests'],
    'author': 'Lichun',
    'long_description': long_description,
    'url': 'https://github.com/socrateslee/pyuque',
    'classifiers': [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if __name__ == '__main__':
    setup(**sdict)
