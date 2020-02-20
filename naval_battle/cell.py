class Cell:
    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return self.status.value
