import argparser
from collections import namedtuple
from possible_shot_result import PossibleShotResult
import sys
import random
from board import Board
import pickle
import os


Launch_args = namedtuple('Launch_args', [
    'width',
    'height',
    'user_board',
    'opponent_board',
    'opponents_visible_board',
    'user_shots',
    'computer_shots'
])


def main(width, height):
    users_board = Board(width, height)
    opponent_board = Board(width, height)
    opponents_visible_board = Board(width, height)
    opponent_board.refresh_board()
    opponents_visible_board.create_board()
    computer_shots = set()
    user_shots = set()
    consent = input('Для объяснения введи \'help\' для продолжения любую клавишу\n')

    if consent == 'help':
        print(f'''Это игра Морской бой
        Ты играешь против компьютера
        Для выхода с сохранением значений игры введи \'save\'
        Для выхода без сохранения \'exit\'
        ''')
        input('для продолжения любую клавишу\n')

    while consent != 'ок':
        users_board.refresh_board()
        users_board.print_board(opponents_visible_board)
        consent = input('Если ты доволен полем пиши \'ок\' и жмякай Enter\n')
    args = Launch_args(width, height, users_board, opponent_board, opponents_visible_board, user_shots, computer_shots)
    run(args)


def run(args):
    while True:
        row_input = input('Введи координаты пальбы или команду\n')
        if row_input == 'save':
            save_state(args)
            sys.exit(0)

        if row_input == 'exit':
            my_exit()

        try:
            row_x, row_y = row_input.split()
            x = int(row_x)
            y = int(row_y)
        except ValueError:
            print('Ты где-то зафакапил с вводом, попробуй снова')
            continue

        if x >= args.width or x < 0 or y >= args.height or y < 0:
            print('В молочко, прицелься лучше')
            continue

        if (x, y) not in args.user_shots:
            args.user_shots.add((x, y))
            if check_and_mark_hit_ships(args.opponent_board, x, y, True, args.opponents_visible_board):
                args.user_board.print_board(args.opponents_visible_board)
                if args.opponent_board.count_ship == 0:
                    print('Ты красавчик, ты замочил все корабли компуктера!!')
                    my_exit()
                continue
        else:
            print('Ты сюда уже стрелял, не надо так')
            continue

        args.user_board.print_board(args.opponents_visible_board)
        print(f'\nХод компуктера')
        computer_shot(args)
        args.user_board.print_board(args.opponents_visible_board)


def computer_shot(args):
    while True:
        x, y = generate_coordinates(args)
        if check_and_mark_hit_ships(args.user_board, x, y):
            if args.user_board.count_ship == 0:
                print('Выиграл компуктер')
                args.user_board.print_board(args.opponent_board)
                my_exit()
            continue
        return


def generate_coordinates(args):
    while True:
        x = random.randint(0, args.width - 1)
        y = random.randint(0, args.height - 1)
        if (x, y) not in args.computer_shots:
            args.computer_shots.add((x, y))
            return x, y


def my_exit():
    if os.path.exists('data.pickle'):
        os.remove('data.pickle')
    sys.exit(0)


def check_and_mark_hit_ships(board, x, y, is_opposite=False, blackboard=None):
    for ship in board.ships:
        for location in ship.location:
            if location[0] == x and location[1] == y:
                info = ship.ships_hit()
                if info == PossibleShotResult.KILLED:
                    board.count_ship -= 1
                print(info.value)
                board.mark_hit(x, y, True, is_opposite, blackboard)
                return True
    print(PossibleShotResult.MISS.value)
    board.mark_hit(x, y, False, is_opposite, blackboard)

    return False


def save_state(args):
    list_state = [args.width, args.height, args.user_board, args.blackboard,
                  args.opponent_board, args.user_shots, args.computer_shots]
    with open('data.pickle', 'wb') as f:
        pickle.dump(list_state, f)


def load_state():
    with open('data.pickle', 'rb') as f:
        data_new = pickle.load(f)
        data_new[2].print_board(data_new[4])
        launch_args = Launch_args(data_new[0], data_new[1], data_new[2], data_new[3], data_new[4], data_new[5], data_new[6])
    run(launch_args)


if __name__ == '__main__':
    height_width_args = argparser.parse_args()
    if height_width_args.width < 5 or height_width_args.height < 5:
        print('Некорректная размерность поля')
        sys.exit(0)
    if os.path.exists('data.pickle'):
        inp = input('Хочешь продолжить там, где закончил? введи \'да\' или \'нет\'\n')
        if inp == 'да':
            load_state('data.pickle')
    main(height_width_args.width, height_width_args.height)
