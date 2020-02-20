from enum import Enum


class CellsState(Enum):
    SEA = '≈'
    SHIP = '■'
    BROKEN_SHIP = 'ν'
    MISS = '×'
