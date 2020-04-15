import os
from PIL import Image
from typing import Tuple
from base64 import b64encode, b64decode
from image_resizer.config import redis_conn as redis


def task_run(images_id: str, byte_image: str) -> None:
    redis.set(f'{images_id}_original',  byte_image)
    decode_image(images_id, byte_image)
    res32 = compress_image(images_id, 32)
    res64 = compress_image(images_id, 64)
    redis.mset({res32[0]: res32[1], res64[0]: res64[1]})
    os.remove(f'image_resizer/tmp/{images_id}.jpg')
    os.remove(f'image_resizer/tmp/compr/{images_id}_32.jpg')
    os.remove(f'image_resizer/tmp/compr/{images_id}_64.jpg')


def decode_image(image_id: str, byte_image: str) -> None:
    b_image = b64decode(byte_image)
    with open(f'image_resizer/tmp/{image_id}.jpg', 'wb') as f:
        f.write(b_image)


def compress_image(image_id: str, size: int) -> Tuple[str, str]:
    row_image = Image.open(f'image_resizer/tmp/{image_id}.jpg')
    resize_image = row_image.resize((size, size))
    path = f'image_resizer/tmp/compr/{image_id}_{size}.jpg'
    resize_image.save(path)
    with open(path, 'rb') as f:
        byte_image = f.read()

    return f'{image_id}_{size}', b64encode(byte_image)



