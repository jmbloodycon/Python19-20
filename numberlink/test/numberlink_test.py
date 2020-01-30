import unittest
import numberlink as numb
from Graph import Node


class NumberlinkTests(unittest.TestCase):
    def test_points_incorrect_with_size(self):
        point = numb.is_point_correct('11 2', '3 4', 5)
        self.assertEqual(point, False)

    def test_points_correct(self):
        point = numb.is_point_correct('1 2', '3 4', 5)
        self.assertEqual(point, ((1, 2), (3, 4)))

    def test_find_solution(self):
        res = numb.find_solution(3, [((0, 0), (2, 2)), ((0, 1), (0, 2))])
        correct_path = {(Node(0, 1), Node(0, 2)): [Node(0, 1), Node(0, 2)],
                        (Node(0, 0), Node(2, 2)):
                            [Node(0, 0), Node(1, 0), Node(2, 0), Node(2, 1),
                             Node(1, 1), Node(1, 2), Node(2, 2)]}
        self.assertEqual(res, (True, correct_path))

    def test_no_solution(self):
        res = numb.find_solution(2, [((0, 0), (1, 1))])
        self.assertEqual(res, (False, {(Node(0, 0), Node(1, 1)): None}))
