import random


class Solver(object):
    def __init__(self, env, x, y, grid, params):
        self.env = env
        self.x = x
        self.y = y
        self.grid = grid
        self.params = params
        self.cleaned = 0
        self.strategy = params.strategy_class(self)
        self.env.process(self.search())

    @staticmethod
    def id():
        return 2

    def search(self):
        while True:
            new_direction = self.strategy.apply()
            self.move_to(*new_direction)
            yield self.env.timeout(4)

    def move_to(self, x, y):
        self.grid.data[self.x, self.y, 0] = 0
        self.grid.data[x, y, 0] = Solver.id()
        self.x = x
        self.y = y
