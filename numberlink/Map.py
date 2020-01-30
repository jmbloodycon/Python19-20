from Graph import Node
import copy
from typing import List, Tuple, Union, Dict


class Map:
    STACK = []
    COLORS = [(255, 0, 0),
              (0, 255, 255),
              (255, 0, 255),
              (0, 128, 0),
              (0, 0, 128),
              (255, 255, 255),
              (255, 255, 0),
              (0, 0, 255),
              (128, 0, 0),
              (0, 255, 0)
              ]

    def __init__(self, size: int) -> None:
        """Создает экземпляр игровой карты"""
        self.size = size
        self.square = size * size
        self.dict_nodes = {}
        for i in range(size):
            for j in range(size):
                self.dict_nodes[(i, j)] = Node(i, j)
        self.all_paths = {}

    def make_graph(self) -> None:
        """Соединяет соседние вершины ребрами"""
        for i in range(self.size):
            for j in range(self.size):
                if i - 1 >= 0:
                    self.dict_nodes[(i, j)].connect(self.dict_nodes[(i-1, j)])
                if j - 1 >= 0:
                    self.dict_nodes[(i, j)].connect(self.dict_nodes[(i, j-1)])
                if j + 1 < self.size:
                    self.dict_nodes[(i, j)].connect(self.dict_nodes[(i, j+1)])
                if i + 1 < self.size:
                    self.dict_nodes[(i, j)].connect(self.dict_nodes[(i+1, j)])

    def mark_ends(self, pairs: List[Union[Tuple[Tuple[int, int],
                                          Tuple[int, int]], bool]]) -> None:
        """Помечает концы путей, задает цвет"""
        count = 0
        for i in pairs:
            color = self.COLORS[count]
            count += 1
            self.dict_nodes[i[0]].mark_end(self.dict_nodes[i[1]])
            self.dict_nodes[i[0]].color = color
            self.dict_nodes[i[1]].mark_end(self.dict_nodes[i[0]])
            self.dict_nodes[i[1]].color = color

    def find_all_paths(self,
                       pairs: List[Union[Tuple[Tuple[int, int],
                                               Tuple[int, int]],
                                         bool]]) \
            -> Dict[Tuple[Node, Node], List[List[Node]]]:
        """Находит все возможные пути для всех пар,
         не проходящие через другие пары"""
        for pair in pairs:
            start = self.dict_nodes[pair[0]]
            self.STACK = [start]
            self.open_node(start, start)
        return self.all_paths

    def open_node(self, start: Node, node: Node) -> None:
        """Раскрывает вершину"""
        if node.is_end and node != start:
            if node.other_end == start:
                self.save_path((start, node))
            return
        for e in node.edges:
            op_node = e.get_opposite_node(node)
            if op_node not in self.STACK:
                self.STACK.append(op_node)
                self.open_node(start, op_node)
                self.STACK.pop()

    def save_path(self, pair: Tuple[Node, Node]) -> None:
        """Сохраняет путь в словарь всех путей"""
        if pair not in self.all_paths:
            self.all_paths[pair] = []
        self.all_paths[pair].append(copy.deepcopy(self.STACK))
