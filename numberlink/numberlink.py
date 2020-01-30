import re
from Graph import Node
from Map import Map
import Drawing as d
import Video as v
from typing import Dict, List, Tuple, Union

r = re.compile(r'\d+ \d+')


def configure_game() -> None:
    """Эта основная функция решаеля. Запрашивает у пользвателя размерность,
    количство пар и координаты конечных точек в каждой паре.
    Ищет решение"""
    size = 0
    pair_count = 0
    pairs = []
    while size < 2 or size > 10:
        try:
            size = int(input('Введите размерность от 2 до 10 \n'))
        except ValueError:
            continue

    while pair_count < 1 or pair_count > size * size // 2:
        try:
            pair_count = int(input('Введите количество пар точек\n'))
        except ValueError:
            continue

    for pair in range(pair_count):
        while True:
            start = input(f'введите координаты первой точки в {pair} паре\n')
            end = input(f'введите координаты второй точки в {pair} паре\n')
            current_pair = is_point_correct(start, end, size)
            if current_pair:
                break
            print('Некорректно, давай по новой')
        pairs.append(current_pair)

    res = find_solution(size, pairs)

    if res[0]:
        color_paths(res[1])
        d.draw_picture(size, res[1])
        v.make_video()


def color_paths(paths: Dict[Tuple[Node, Node], List[Node]]) -> None:
    """Окрашивает все пути в цвет, соответствующий начальной точке"""
    for key in paths:
        color = paths[key][0].color
        for node in paths[key][1:]:
            node.color = color


def find_solution(size: int,
                  pairs: List[Union[Tuple[Tuple[int, int],
                                          Tuple[int, int]], bool]]) \
        -> Tuple[bool, Dict[Tuple[Node, Node], List[Node]] or str]:
    """Эта функция ищет решение головоломки по листу всех пар"""
    i_map = Map(size)
    i_map.make_graph()
    i_map.mark_ends(pairs)
    all_paths = i_map.find_all_paths(pairs)

    if len(all_paths.keys()) < len(pairs):
        return False, 'Нет решений'

    right_paths = find_right_combination(all_paths, i_map.square)
    return right_paths


def find_right_combination(all_path: Dict[Tuple[Node, Node], List[List[Node]]],
                           volume: int):
    """Эта функция ищет корректную комбинацию путей"""
    pairs = list(all_path.keys())
    start_pair = pairs.pop()
    return right_combination_finder(start_pair, set(),
                                    pairs, all_path, volume, {})


def right_combination_finder(current_pair: Tuple[Node, Node], busy_nodes: set,
                             pairs: List[Tuple[Node, Node]],
                             all_paths: Dict[Tuple[Node, Node],
                                             List[List[Node]]],
                             volume: int,
                             right_paths: None or Dict[Tuple[Node, Node],
                                                       List[Node]]) \
        -> Dict[Tuple[Node, Node], List[Node]] or Tuple[bool,
                                                        Dict[Tuple[Node, Node],
                                                             List[Node]]]:
    """Рекурсивный метод комбинирования путей"""
    for path in all_paths[current_pair]:
        set_path = set(path)
        if len(set_path & busy_nodes) != 0:
            continue
        right_paths[current_pair] = path
        busy_nodes |= set_path
        if len(pairs) == 0:
            if len(busy_nodes) == volume:
                return True, right_paths
            else:
                right_paths[current_pair] = None
                busy_nodes -= set_path
                continue
        next_pair = pairs.pop()
        result = right_combination_finder(next_pair,
                                          busy_nodes, pairs, all_paths,
                                          volume, right_paths)
        if not result[0]:
            right_paths[current_pair] = None
            busy_nodes -= set_path
            continue
        else:
            return result

    pairs.append(current_pair)
    return False, right_paths


def is_point_correct(start: str, end: str, size: int) \
        -> Tuple[Tuple[int, int], Tuple[int, int]] or None:
    """Проверка на корректность вводимых точек"""
    if r.match(start) and r.match(end):
        start_x, start_y = start.split()
        end_x, end_y = end.split()
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)
        if not (start_x < 0 or start_x > size
                or start_y < 0 or start_y > size
                or end_x < 0 or end_x > size
                or end_y < 0 or end_y > size):
            return (start_x, start_y), (end_x, end_y)
    return False


if __name__ == '__main__':
    configure_game()
