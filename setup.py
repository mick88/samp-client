#!/usr/bin/env python
from setuptools import setup

try:
    long_description = open('README.md', 'r').read()
except:
    long_description = ''

setup(
    name='samp-client',
    version='3.0.1',
    packages=['samp_client'],
    url='https://github.com/mick88/samp-client',
    license='MIT',
    author='Michal Dabski',
    author_email='contact@michaldabski.com',
    install_requires=[],
    description='SA-MP API client for python supporting both query and RCON APIs',
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Source': 'https://github.com/mick88/samp-client',
        'Tracker': 'https://github.com/mick88/samp-client/issues',
    },
)
