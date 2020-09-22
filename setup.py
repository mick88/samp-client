#!/usr/bin/env python
from setuptools import setup

try:
    long_description = open('README.md', 'r').read()
except:
    long_description = ''

setup(
    name='samp-client',
    version='2.1.1',
    packages=['samp_client'],
    url='https://github.com/mick88/samp-client',
    license='MIT',
    author='Michal Dabski',
    author_email='contact@michaldabski.com',
    install_requires=['future'],
    description='SA-MP API client for python supporting both query and RCON APIs',
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
