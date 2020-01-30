import unittest
from Monster import Monster
from game_window import TypingTutor
from game_window import Game
from Player import Player
import game_window
import pygame


class TypingTutorTests(unittest.TestCase):
    def test_monsters_name(self):
        monster = Monster('Кристина', 0.12, 0.12, 'Christina.png', (10, 10))
        self.assertEqual(monster.name, 'Кристина')

    def test_kill_all_monsters(self):
        monster = Monster('Кристина', 0.12, 0.12, 'Christina.png', (10, 10))
        monster.kill_monster()
        self.assertEquals(monster.is_alive, False)

    def test_player_init(self):
        player = Player('monica', 12, False)
        self.assertEquals(player.name, 'monica')

    def test_kill_monster(self):
        monsters = {Monster('Гоша', 0.05, -0.05, 'Gosha.png',
                            (10, 480)): [[], [1, 2]]}
        tutor = Game()
        tutor.kill_monster('Гоша', monsters)
        self.assertEquals(list(monsters.keys())[0].is_alive, False)

    def test_choose_winner(self):
        players = [Player('kek', 12, False), Player('lol', 14, False)]
        game = TypingTutor()
        winner = game.choose_winner(players)
        self.assertEquals(winner, 'kek')

    def test_get_blit(self):
        pygame.init()
        BLACK = (0, 0, 0)
        text_im = game_window.get_object_blit('lol', 12, 10, 2, 'arial', BLACK)
        center = (12, 10)
        self.assertEquals(text_im[0].center, center)

    def test_make_digit_text(self):
        game = TypingTutor()
        result_text = game.make_text('g', '', True)
        self.assertEquals(result_text, '')

    def test_make_text(self):
        game = TypingTutor()
        result_text = game.make_text('k', 'ke', False)
        self.assertEquals(result_text, 'kek')
