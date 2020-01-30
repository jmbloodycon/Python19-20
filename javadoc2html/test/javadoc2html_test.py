import unittest
import javadoc2html
import os


class Javadoc2HtmlTests(unittest.TestCase):
    def test_to_page(self):
        res = javadoc2html.to_page('lol')
        exce = f'<!DOCTYPE html><html><head>'\
            f'<meta charset="utf-8"><title>Javadoc</title></head>'\
            f'<body>lol</body></html>'
        self.assertEqual(exce, res)

    def test_save_html(self):
        javadoc2html.save_html('lol', '<h1>lol</hl>')
        self.assertEqual(True, os.path.exists('lol.html'))

    def test_run(self):
        javadoc2html.run()
        self.assertEqual(True, os.path.exists('mod.html'))
