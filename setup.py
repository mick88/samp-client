#!/usr/bin/env python
import os
from distutils.core import setup


def get_version():
    import subprocess
    version = subprocess.check_output('git describe --always --tags'.split(' '), cwd=os.path.dirname(__file__) or None).strip()
    version = version.split('-')
    if len(version) == 1:
        return version[0]
    else:
        return '{0}.dev{1}'.format(*version)


setup(
    name='samp-client',
    version=get_version(),
    packages=['samp_client'],
    url='https://github.com/mick88/samp-client',
    license='MIT',
    author='Michal Dabski',
    author_email='contact@michaldabski.com',
    description='SA-MP API client for python supporting both query and RCON APIs',
    long_description=open('README.md', 'r').read(),
)
