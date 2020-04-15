from base64 import b64encode
from image_resizer.compress_image import task_run, compress_image, decode_image
from os import path


def test_decode_image():
    with open('tests/1.jpg', 'rb') as f:
        image = f.read()
    byte_image = b64encode(image)
    decode_image('1', byte_image)

    assert path.exists('image_resizer/tmp/')


def test_compress_image():
    compress_image('1', 64)
    assert path.exists('image_resizer/tmp/compr/1_64.jpg')

