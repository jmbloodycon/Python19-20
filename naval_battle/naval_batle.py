import argparser
import sys
import random
from board import Board
import pickle
import os


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

    run(width, height, users_board, opponent_board, opponents_visible_board, user_shots, computer_shots)


def run(width, height, users_board, opponent_board, opponents_visible_board, user_shots, computer_shots):
    while True:
        row_input = input('Введи координаты пальбы или команду\n')
        if row_input == 'save':
            save_state(width, height, users_board, opponent_board,
                       opponents_visible_board, user_shots, computer_shots)
            sys.exit(0)

        if row_input == 'exit':
            my_exit()

        try:
            row_x, row_y = row_input.split()
            x = int(row_x)
            y = int(row_y)
        except Exception:
            print('Ты где-то зафакапил с вводом, попробуй снова')
            continue

        if x >= width or x < 0 or y >= height or y < 0:
            print('В молочко, прицелься лучше')
            continue

        if not (x, y) in user_shots:
            user_shots.add((x, y))
            if check_and_mark_hit_ships(opponent_board, x, y, True, opponents_visible_board):
                if opponent_board.count_ship == 0:
                    print('Ты красавчик, ты замочил все корабли компуктера!!')
                    users_board.print_board(opponent_board)
                    my_exit()
                continue
        else:
            print('Ты сюда уже стрелял, не надо так')
            continue

        print(f'\nХод компуктера')
        computer_shot(users_board, width, height, computer_shots, opponent_board)
        users_board.print_board(opponents_visible_board)


def computer_shot(user_board, width, height, computer_shots, opponent_board):
    while True:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if not (x, y) in computer_shots:
            computer_shots.add((x, y))
            if check_and_mark_hit_ships(user_board, x, y):

                if user_board.count_ship == 0:
                    print('Выиграл компуктер')
                    user_board.print_board(opponent_board)
                    my_exit()
                computer_shot(user_board, width, height, computer_shots, opponent_board)
            return


def my_exit():
    if os.path.exists('data.pickle'):
        os.remove('data.pickle')
    sys.exit(0)


def check_and_mark_hit_ships(board, x, y, is_opposite=False, blackboard=None):
    for ship in board.ships:
        for location in ship.location:
            if location[0] == x and location[1] == y:
                info = ship.ships_hit()
                if info == 'Убил':
                    board.count_ship -= 1
                print(info)
                board.mark_hit(x, y, True, is_opposite, blackboard)
                return True
    print('Мимо')
    board.mark_hit(x, y, False, is_opposite, blackboard)
    return False


def save_state(width, height, user_board, blackboard, opponent_board, user_shots, computer_shots):
    list_state = [width, height, user_board, blackboard, opponent_board, user_shots, computer_shots]
    with open('data.pickle', 'wb') as f:
        pickle.dump(list_state, f)


def load_state(data):
    with open('data.pickle', 'rb') as f:
        data_new = pickle.load(f)
        data_new[2].print_board(data_new[4])
    run(data_new[0], data_new[1], data_new[2], data_new[3], data_new[4], data_new[5], data_new[6])


if __name__ == '__main__':
    args = argparser.parse_args()
    if args.width < 5 or args.height < 5:
        print('Некорректная размерность поля')
        sys.exit(0)
    if os.path.exists('data.pickle'):
        inp = input('Хочешь продолжить там, где закончил? введи \'да\' или \'нет\'\n')
        if inp == 'да':
            load_state('data.pickle')
    main(args.width, args.height)
