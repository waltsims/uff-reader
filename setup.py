#!/usr/bin/env python

from distutils.core import setup

setup(name='UFF.py',
      version='0.1',
      description='Python interface for the Ultrasound File Format (UFF)',
      author='Walter Simson',
      author_email='walter.simson@tum.de',
      #url='',
      packages=['uff'],
      package_dir = {'':'src'}
     )


