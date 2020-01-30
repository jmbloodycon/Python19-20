import pygame
from Monster import Monster
import sys
import time
from Player import Player


BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)


def get_object_blit(text, x, y, size, font, color):
    """The function creates an object for drawing
    text according to specified parameters."""
    obj = pygame.font.SysFont(font, size)
    text_amateur = obj.render(text, True, color, "None")
    text_rect = text_amateur.get_rect()
    text_rect.center = (x, y)

    return (text_rect, text_amateur)


class TypingTutor:
    PLAYERS = []

    def run(self):
        """The function starts all components of the program."""
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.flip()
        players_count = int(self.request_players_info('Enter count of players',
                                                      True))
        for i in range(players_count):
            name = self.request_players_info('Enter the name of player', False)
            game = Game()
            result = game.new_game()
            self.PLAYERS.append(Player(name, result[0], result[1]))
        self.make_winner()

    def request_players_info(self, title, digit):
        """The function prompts the user for
        the number of players or
        his name  in graphic mode."""
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("tut kakaya-to dich")
        background_image = pygame.image.load("horror_bg.jpg")
        text_image = get_object_blit(title, 300,
                                     60, 40, 'arial', WHITE)
        flag = True
        text = ''

        while flag:
            screen.blit(background_image, [0, 0])
            screen.blit(text_image[1], text_image[0])
            pygame.draw.rect(screen, WHITE, (220, 320, 160, 40))
            text_im = get_object_blit(text, 300, 340, 20, 'arial', BLACK)
            screen.blit(text_im[1], text_im[0])
            pygame.display.update()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit(0)

                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_BACKSPACE:
                        if text == '':
                            continue
                        text = text[:-1]

                    if i.key == pygame.K_RETURN:
                        if text == '':
                            continue
                        flag = False
                    else:
                        text = self.make_text(i.unicode, text, digit)

        return text

    def make_text(self, char, text, digit):
        """The function creates text based on the key
         pressed and prompted to enter."""
        if digit:
            if char.isdigit():
                text += char
        else:
            text += char
        return text

    def make_winner(self):
        """The function draws the name of the winner."""
        winner = self.choose_winner(self.PLAYERS)
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("tut kakaya-to dich")
        background_image = pygame.image.load("winner.jpg")
        text_image = get_object_blit('WINNER IS', 300, 60, 60, 'arial', SILVER)
        text_im = get_object_blit(winner, 300, 250, 50, 'arial', SILVER)
        flag = True

        while flag:
            screen.blit(background_image, [0, 0])
            screen.blit(text_image[1], text_image[0])
            screen.blit(text_im[1], text_im[0])
            pygame.display.update()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit(0)

    def choose_winner(self, players):
        """The function selects the winner from
        a given sheet of players in time, if any."""
        winners = []
        for player in players:
            if not player.dead:
                winners.append(player)
        if len(winners) == 0:
            return 'Nobody won'

        return sorted(winners, key=lambda x: x.time)[0].name


class Game:
    def __init__(self):
        self.MONSTERS = [
            Monster('Кристина', 0.12, 0.12, 'Christina.png', (10, 10)),
            Monster('Софья', 0.08, 0, 'Sofa.png', (10, 280)),
            Monster('Гоша', 0.05, -0.05, 'Gosha.png', (10, 480)),
            Monster('Глеб', -0.19, - 0.19, 'Gleb.png', (480, 480)),
            Monster('Моника', -0.01, 0, 'monica.png', (480, 280)),
            Monster('Сеня', -0.1, 0.1, 'Senya.png', (480, 10)),
            ]

    def new_game(self):
        """The function draws monstrik and monitors their
        location on the screen, as well as tracks the keyboard.
        The main function of the game for the user."""
        pygame.init()
        dead = False
        screen = pygame.display.set_mode((600, 600))
        pygame.display.flip()
        pygame.display.set_caption("tut kakaya-to dich")
        background_image = pygame.image.load("horror_bg.jpg")
        monster_name = []
        monsters = {}

        for unit in self.MONSTERS:
            monsters[unit] = (pygame.image.load(unit.image),
                              unit.start_position)
            monster_name.append(unit.name)

        text = ''
        text_image = get_object_blit(text, 10, 60, 60, 'arial', WHITE)
        player_image = pygame.image.load('gamer.png')
        dead_text_image = pygame.image.load('empty.png')
        stop = False
        flag = True
        dead_monster_count = 0
        start_time = time.time()

        while flag:
            screen.blit(background_image, [0, 0])
            screen.blit(player_image, (250, 250))
            screen.blit(dead_text_image, (160, 480))

            if dead_monster_count == len(monsters.keys()):
                background_image = pygame.image.load("win.jpg")
                dead_text_image = pygame.image.load('win_text.png')
                flag = False

            for unit in monsters:
                if stop:
                    unit.kill_monster()
                    text = ''
                    flag = False
                else:
                    current_text = get_object_blit(unit.name,
                                                   monsters[unit][1][0] + 100,
                                                   monsters[unit][1][1] + 100,
                                                   20, 'arial', WHITE)
                    screen.blit(monsters[unit][0], (monsters[unit][1][0],
                                                    monsters[unit][1][1]))
                    screen.blit(current_text[1], current_text[0])
                    if monsters[unit][1][0] >= 180 and \
                            monsters[unit][1][0] <= 330:
                        if monsters[unit][1][1] >= 230 and \
                                monsters[unit][1][1] <= 320:
                            player_image = pygame.image.load('dead_g.png')
                            background_image = pygame.image.load("dead_bg.jpg")
                            dead_text_image = pygame.image.load('dead_t.png')
                            stop = True
                            dead = True

                monsters[unit] = (monsters[unit][0],
                                  (monsters[unit][1][0] + unit.dx,
                                   monsters[unit][1][1] + unit.dy))
            screen.blit(text_image[1], text_image[0])
            pygame.display.update()

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit(0)

                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        text_image = get_object_blit(text, 280, 580,
                                                     30, 'arial', WHITE)
                    else:
                        text += i.unicode
                        text_image = get_object_blit(text, 280, 580,
                                                     30, 'arial', WHITE)
                        if text in monster_name:
                            dead_monster_count += 1
                            monster_name.remove(text)
                            text = self.kill_monster(text, monsters)

        screen.blit(background_image, [0, 0])
        screen.blit(player_image, (250, 250))
        screen.blit(dead_text_image, (160, 480))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.event.clear()

        return (time.time() - start_time, dead)

    def kill_monster(self, name, monsters):
        """The function kills monsters from the monsters
        set according to the entered name."""
        for monster in monsters:
            if monster.name == name:
                monsters[monster] = \
                    (pygame.image.load(
                        monster.dead_monster_image),
                     (monsters[monster][1][0],
                      monsters[monster][1][1]))
                monster.kill_monster()

        return ''


if __name__ == '__main__':
    tutor = TypingTutor()
    tutor.run()
