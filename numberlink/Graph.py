import typing


class Node:
    """Класс вершины"""
    is_end = False
    other_end = None
    color = None

    def __init__(self, x, y) -> None:
        self.number = (x, y)
        self.edges = []

    def connect(self, other_node) -> None:
        """Соединяет вершину с соседней,
        добавляет рбро в список инцидентных ребер"""
        edge = Edge(self, other_node)
        if edge not in self.edges:
            self.edges.append(edge)
            other_node.edges.append(edge)

    def mark_end(self, end) -> None:
        """помеяает первую и последнюю точку концами пути"""
        self.is_end = True
        self.other_end = end

    def __eq__(self, other) -> bool:
        return other.number == self.number

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self) -> str:
        return str(self.number)


class Edge:
    """Класс ребра"""
    def __init__(self, start: typing.Optional[Node],
                 end: typing.Optional[Node]) -> None:
        self.start = start
        self.end = end

    def get_opposite_node(self, node: typing.Optional[Node])\
            -> typing.Optional[Node] or None:
        """Возвращает противоположную вершину """
        if node == self.start:
            return self.end
        if node == self.end:
            return self.start
        return

    def __eq__(self, other) -> bool:
        return (other.start == self.start and other.end == self.end) or \
               (other.end == self.start and other.start == self.end)
