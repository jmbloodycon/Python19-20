import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog='naval_battle.py', description='Размерность поля')
    parser.add_argument('width', type=int, help='Ширина', default=10, action='store')
    parser.add_argument('height', type=int, help='Высота', default=10, action='store')
    return parser.parse_args()
