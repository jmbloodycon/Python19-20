import unittest
from Map import Map
from Graph import Node


class MapTests(unittest.TestCase):
    def test_init(self):
        i_map = Map(5)
        self.assertEqual(i_map.square, 25)

    def test_make_graph(self):
        i_map = Map(2)
        i_map.make_graph()
        self.assertEqual(i_map.dict_nodes[(0, 0)], Node(0, 0))

    def test_mark_end(self):
        i_map = Map(2)
        i_map.make_graph()
        i_map.mark_ends([((0, 0), (1, 0))])
        self.assertEqual(i_map.dict_nodes[(0, 0)].other_end, Node(1, 0))

    def test_find_all_path(self):
        i_map = Map(2)
        i_map.make_graph()
        i_map.mark_ends([((0, 0), (1, 0))])
        i_map.find_all_paths([((0, 0), (1, 0))])
        all_path = {(Node(0, 0), Node(1, 0)): [[Node(0, 0), Node(0, 1),
                                                Node(1, 1), Node(1, 0)],
                                               [Node(0, 0), Node(1, 0)]]}
        self.assertEqual(i_map.all_paths[(Node(0, 0), Node(1, 0))][1],
                         all_path[(Node(0, 0), Node(1, 0))][1])
