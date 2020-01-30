from PIL import Image
from PIL import ImageDraw
from Graph import Node
import shutil
import os
from typing import Tuple, Dict, List


def draw_picture(size: int,
                 paths: Dict[Tuple[Node, Node], List[Node]]) -> None:
    """Эта функция отрисовывает все пути в соотвествии со словарем"""
    if os.path.exists('tmp'):
        shutil.rmtree("tmp")
    os.mkdir("./tmp")
    image = Image.new('RGB', (50 * size, 50 * size), "black")
    draw = ImageDraw.ImageDraw(image)
    count = 0
    for pair in paths:
        for point in pair:
            draw.rectangle(
                [(point.number[0] * 50, point.number[1] * 50),
                 (point.number[0] * 50 + 50, point.number[1] * 50 + 50)],
                fill=point.color)
    cell_map(size, image, (192, 192, 192))
    image.save(f'tmp/{count}.jpg')
    count += 1
    for key in paths:
        for node in paths[key][1:-1]:
            draw.rectangle([(node.number[0]*50, node.number[1]*50),
                            (node.number[0]*50+50, node.number[1]*50+50)],
                           fill=node.color)

            cell_map(size, image, (192, 192, 192))
            image.save(f'tmp/{count}.jpg')
            count += 1
    image.save('grid_img.png', 'PNG')


def cell_map(size: int, img: Image, color: Tuple[int, int, int]) -> Image:
    """Разлиновывет поле"""
    draw = ImageDraw.Draw(img)
    for i in range(50, 50 * size, 50):
        draw.line([(i, 0), (i, 50 * size - 1)], fill=color, width=2)
        for j in range(50, 50 * size, 50):
            draw.line([(0, j), (50 * size - 1), j], fill=color, width=2)

    return img
