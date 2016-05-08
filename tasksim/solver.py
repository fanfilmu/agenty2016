import random
from task import Task


class Solver(object):
    def __init__(self, env, x, y, grid, params):
        self.env = env
        self.x = x
        self.y = y
        self.grid = grid
        self.params = params
        self.env.process(self.search())

    @staticmethod
    def id():
        return 2

    def search(self):
        while True:
            max_smells = (-1, [])
            for x in xrange(self.x - 1, self.x + 2):
                for y in range(self.y - 1, self.y + 2):
                    if x < 0 or x >= self.params.width:
                        continue
                    if y < 0 or y >= self.params.height:
                        continue

                    if self.grid.data[x, y, 0] == 0:
                        if self.grid.data[x, y, 1] == max_smells[0]:
                            max_smells[1].append((x, y))
                        elif self.grid.data[x, y, 1] > max_smells[0]:
                            max_smells = (self.grid.data[x, y, 1], [(x, y)])
                    elif self.grid.data[x, y, 0] == Task.id():
                        self.grid.clear_task_at(x, y)

            new_direction = random.sample(max_smells[1], 1)[0]
            self.move_to(*new_direction)
            yield self.env.timeout(4)

    def move_to(self, x, y):
        self.grid.data[self.x, self.y, 0] = 0
        self.grid.data[x, y, 0] = Solver.id()
        self.x = x
        self.y = y
