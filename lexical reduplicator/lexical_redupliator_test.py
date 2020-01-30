import unittest
from lexicalReduplicate import LexicalReduplicate


class LexicalReduplicateTests(unittest.TestCase):
    def test_rediplication(self):
        redup = LexicalReduplicate()
        example = 're.txt'
        self.assertEqual(example, redup.file_name)

    def test_make_reduplication(self):
        redup = LexicalReduplicate()
        redup.prefixes = ['бажу', 'бажу', 'бажу']
        example = redup.make_reduplication()
        self.assertEqual(example[0], 'Привет-бажувет')

    def test_make_reduplication_short_word(self):
        redup = LexicalReduplicate()
        redup.prefixes = ['бажу', 'бажу', 'бажу']
        example = redup.make_reduplication()
        self.assertEqual(example[1], 'Хай')

    def test_word_analyze(self):
        redup = LexicalReduplicate()
        example = redup.word_analyze('Привет', 'хуе')
        self.assertEqual(example, 'Привет-хуивет')

    def test_word_analyze_with_punctuation(self):
        redup = LexicalReduplicate()
        example = redup.word_analyze('Привет,', 'хуе')
        self.assertEqual(example, 'Привет-хуивет,')

    def test_word_analyze_with_hyphenated_and_punctuation(self):
        redup = LexicalReduplicate()
        example = redup.word_analyze('Когда-нибудь,', 'хуе')
        self.assertEqual(example, 'Когда-нибудь-хуёгда-нибудь,')

    def test_change_prefix_e(self):
        redup = LexicalReduplicate()
        example = redup.change_prefix_form('холе', 'ать')
        self.assertEqual(example, 'холя')

    def test_change_prefix_i(self):
        redup = LexicalReduplicate()
        example = redup.change_prefix_form('холе', 'ить')
        self.assertEqual(example, 'холи')

    def test_change_prefix_o(self):
        redup = LexicalReduplicate()
        example = redup.change_prefix_form('холе', 'оть')
        self.assertEqual(example, 'холё')

    def test_not_change_prefix(self):
        redup = LexicalReduplicate()
        example = redup.change_prefix_form('холе', 'дать')
        self.assertEqual(example, 'холе')
