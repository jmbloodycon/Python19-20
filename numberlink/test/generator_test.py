import unittest
from Map import Map
import numberlink_generator as gen


class GeneratorTests(unittest.TestCase):
    def test_generator(self):
        pairs = gen.generate(6)
        self.assertEqual(len(pairs), 6)

    def test_create_initial_path(self):
        i_map = Map(2)
        i_map.make_graph()
        path_list = gen.create_initial_paths(2, i_map)
        self.assertEqual(len(path_list), 2)

    def test_mark_end(self):
        i_map = Map(2)
        i_map.make_graph()
        path_list = gen.create_initial_paths(2, i_map)
        gen.mark_end(path_list)
        self.assertEqual(path_list[0][0].is_end, True)

    def test_color_ends(self):
        i_map = Map(2)
        i_map.make_graph()
        dict_pairs = {}
        path_list = gen.create_initial_paths(2, i_map)
        gen.color_pairs(path_list, dict_pairs)
        self.assertEqual(path_list[0][0].color, (255, 0, 0))
