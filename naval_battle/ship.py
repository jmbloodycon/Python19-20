from cells_state import CellsState
from possible_shot_result import PossibleShotResult


class Ship:
    def __init__(self, location, count):
        self.location = location
        self.count_alive_cell = count
        self.is_alive = True

    def ships_hit(self):
        if self.is_alive:
            self.count_alive_cell -= 1
            if self.count_alive_cell == 0:
                self.is_alive = False
            else:
                return PossibleShotResult.HIT
        return PossibleShotResult.KILLED

    def mark_board(self, board):
        for i in self.location:
            board[i[1]][i[0]].status = CellsState.SHIP
