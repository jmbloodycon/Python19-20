import unittest
import numberlink as numb
import Drawing
import os
import Video


class DrawingTests(unittest.TestCase):
    def test_drawing(self):
        res = numb.find_solution(2, [((0, 0), (1, 0))])
        Drawing.draw_picture(2, res[1])
        self.assertEqual(True, os.path.exists('tmp'))

    def test_make_video(self):
        numb.find_solution(2, [((0, 0), (1, 0))])
        Video.make_video()
        self.assertEqual(True, os.path.exists('video.avi'))
