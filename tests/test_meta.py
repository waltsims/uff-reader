from uff import __version__


def test_version():
    if type(__version__) is not str:
        raise TypeError("Version string incorrect")

    if __version__ != "0.3.0":
        raise AssertionError(f"Version {__version__} string incorrect")

    pass
