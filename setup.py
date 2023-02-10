from setuptools import setup

setup(
    name='uff-reader',
    version='0.0.1',
    description='Python interface for the Ultrasound File Format (UFF)',
    author='Walter Simson',
    author_email='walter.simson@tum.de',
    packages=['uff'],
    package_dir={'': 'src'},
    install_requires=['numpy>=1.20',
                      'pytest>=6.2.4',
                      'requests>=2.26.0',
                      'h5py>=3.5.0',
                      'scipy>=1.7.0'])
