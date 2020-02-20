from cells_state import CellsState


class Ship:
    is_alive = True

    def __init__(self, location, count):
        self.location = location
        self.count_alive_cell = count

    def ships_hit(self):
        if self.is_alive:
            self.count_alive_cell -= 1
            if self.count_alive_cell == 0:
                self.is_alive = False
            else:
                return 'Попал'
        return 'Убил'

    def mark_board(self, board):
        for i in self.location:
            board[i[1]][i[0]].status = CellsState.SHIP
