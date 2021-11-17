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
from uff.utils import load_uff_dict

# load uff object from uff file <file-name>
uff_object = UFF.deserialize(load_uff_dict('<file-name>'))
```


