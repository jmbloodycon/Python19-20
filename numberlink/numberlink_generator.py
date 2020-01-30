import random
from Graph import Node
import numberlink as num
from Map import Map
import Drawing as d
import Video as v
from typing import Dict, List, Tuple


def generate(size: int) -> Dict[Tuple[Node, Node], List[Node]]:
    """Генерирует карту по входному разверу"""
    i_map = Map(size)
    i_map.make_graph()
    path_list = create_initial_paths(size, i_map)
    mark_end(path_list)

    for _ in range(50):
        current_path = random.choice(path_list)
        witch_end = random.randint(0, 1)

        if len(current_path) < 3:
            continue

        node = current_path.pop(0) if witch_end else current_path.pop()

        current_path[0].is_end = True
        current_path[-1].is_end = True

        while True:
            r_edges = random.choice(node.edges)
            current_node = r_edges.get_opposite_node(node)
            if current_node.is_end:
                break

        current_node.is_end = False
        for path in path_list:
            if current_node in path:
                if current_node == path[0]:
                    path.insert(0, node)
                else:
                    path.append(node)
                break

    dict_pairs = {}
    color_pairs(path_list, dict_pairs)
    num.color_paths(dict_pairs)

    return dict_pairs


def create_initial_paths(size: int, i_map: Map) -> List[List[Node]]:
    """Создает начальные пути"""
    path_list = []
    for _ in range(size):
        path_list.append([])
    for j in range(size):
        for i in range(size):
            path_list[j].append(i_map.dict_nodes[(i, j)])

    return path_list


def mark_end(path_list: List[List[Node]]) -> None:
    """Помечает конечные вершины в пути"""
    for path in path_list:
        path[0].is_end = True
        path[-1].is_end = True


def color_pairs(path_list: List[List[Node]],
                dict_pairs: Dict[Tuple[Node, Node], List[Node]]) -> None:
    """Раскрашивает стартовую точку каждого пути"""
    count = 0
    for path in path_list:
        start = path[0]
        end = path[-1]
        dict_pairs[(start, end)] = path
        color = Map.COLORS[count]
        count += 1
        start.color = color


if __name__ == '__main__':
    dimension = 6
    dict_pairs_with_paths = generate(dimension)
    d.draw_picture(dimension, dict_pairs_with_paths)
    v.make_video()
    print('done')
