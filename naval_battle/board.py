import random
from cells_state import CellsState
from cell import Cell
from ship import Ship


class Board:
    def __init__(self, width, height):
        self.board = []
        self.width = width
        self.height = height
        self.max_ship = 0
        self.ships = []
        self.count_ship = 0

    def create_board(self):
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(Cell(CellsState.SEA))
        min_size = min(self.height, self.width)
        if min_size % 2 == 0:
            self.max_ship = min_size // 2 - 1
        else:
            self.max_ship = min_size // 2

    def refresh_board(self):
        self.board = []
        self.create_board()
        self.arrange_ships()

    def arrange_ships(self):
        self.ships = []
        count = 1
        double_count = 1
        while self.max_ship > 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            direction = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
            ship_list = []
            f = False
            for i in range(self.max_ship):
                if self.check_neighbors(x, y):
                    ship_list.append((x, y))
                    if i == self.max_ship - 1:
                        break
                    x += direction[0]
                    y += direction[1]
                    if x >= self.width or x < 0 or y >= self.height or y < 0:
                        f = True
                        break
                else:
                    f = True
                    break
            if f:
                continue
            ship = Ship(ship_list, self.max_ship)
            self.count_ship += 1
            ship.mark_board(self.board)
            self.ships.append(ship)
            count -= 1
            if count == 0:
                self.max_ship -= 1
                count = double_count + 1
                double_count += 1

    def check_neighbors(self, x, y):
        if self.board[y][x].status == CellsState.SEA:
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i >= self.width or i < 0 or j >= self.height or j < 0:
                        continue
                    if self.board[j][i].status == CellsState.SHIP:
                        return False
            return True
        return False

    def print_board(self, other_board=None):
        if other_board:
            print(f'\nТвоя доска {"  "*self.width} Доска компуктера')
            for i in range(len(self.board)):
                print(f'{" ".join(map(str, self.board[i]))} \t{" ".join(map(str, other_board.board[i]))}')
        else:
            for i in range(len(self.board)):
                print(' '.join(map(str, self.board[i])))

    def mark_hit(self, x, y, hit, is_opposite=False, blackboard=None):
        if hit:
            if is_opposite:
                blackboard.board[y][x].status = CellsState.BROKEN_SHIP
            self.board[y][x].status = CellsState.BROKEN_SHIP
        else:
            if is_opposite:
                blackboard.board[y][x].status = CellsState.MISS
            self.board[y][x].status = CellsState.MISS
