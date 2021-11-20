#!/usr/bin/env python

from distutils.core import setup

# from uff.version import __version__

setup(
    name='UFF.py',
    version='0.3.0',
    description='Python interface for the Ultrasound File Format (UFF)',
    author='Walter Simson',
    author_email='walter.simson@tum.de',
    # url='',
    packages=['uff'],
    package_dir={'': 'src'},
    install_requires=['numpy>=1.20',
                      'pytest>=6.2.4',
                      'requests>=2.26.0',
                      'h5py>=3.5.0'])
