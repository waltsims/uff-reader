import pytest


@pytest.fixture(scope='session')
def uff_sample(tmp_path_factory):
    uff = tmp_path_factory.getbasetemp() / 'sample_image_small.tif'
    img.write_bytes(b'spam')
    return img