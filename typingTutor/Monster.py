class Monster:
    is_alive = True
    dead_monster_image = 'dead.png'

    def __init__(self, name, dx, dy, alive, start_position):
        self.dx = dx
        self.dy = dy
        self.name = name
        self.image = alive
        self.start_position = start_position

    def kill_monster(self):
        """The function zeros the speed of the monster and kills him."""
        self.dx = 0
        self.dy = 0
        self.is_alive = False
