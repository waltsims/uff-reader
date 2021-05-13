#!/usr/bin/env python

from distutils.core import setup
from uff._version import __version__

setup(name='UFF.py',
      version=__version__,
      description='Python interface for the Ultrasound File Format (UFF)',
      author='Walter Simson',
      author_email='walter.simson@tum.de',
      # url='',
      packages=['uff'],
      package_dir={'': 'src'}
      )
