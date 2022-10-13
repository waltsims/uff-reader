# uff.py

Python Reader for the Ultrasound File Format

This python package is based on the standard defined in v0.3.0 of
the [Ultrasound File Format](https://bitbucket.org/ultrasound_file_format/uff/wiki/Home).

## Instalation

to install run:

```pip install git+https://github.com/waltsims/uff.py```

## Getting Started

``` python3
from uff import UFF

# load uff object from uff file <file-name>
uff_object = UFF.load('<file-name>')

# print uff summary
uff_object.summary
```
## Cite
```bibtex
@inproceedings{bernard2018ultrasound,
  title={The ultrasound file format (UFF)-first draft},
  author={Bernard, Olivier and Bradway, David and Hansen, Hendrik HG and Kruizinga, Pieter and Nair, Arun and Perdios, Dimitris and Ricci, Stefano and Rindal, Ole Marius Hoel and Rodriguez-Molares, Alfonso and Stuart, Matthias Bo and others},
  booktitle={2018 IEEE International Ultrasonics Symposium (IUS)},
  pages={1--4},
  year={2018},
  organization={IEEE}
}
```
