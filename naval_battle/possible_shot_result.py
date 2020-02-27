from enum import Enum


class PossibleShotResult(Enum):
    HIT = 'Попал'
    KILLED = 'Убил'
    MISS = 'Мимо'
