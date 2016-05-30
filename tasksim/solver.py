import random
from task import Task
from smell import Smell


class Solver(object):
    def __init__(self, env, x, y, grid, params):
        self.env = env
        self.x = x
        self.y = y
        self.grid = grid
        self.params = params
        self.cleaned = 0
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
                        if self.__total_smell_value(x, y) == max_smells[0]:
                            max_smells[1].append((x, y))
                        elif self.__total_smell_value(x, y) > max_smells[0]:
                            max_smells = (self.grid.data[x, y, 1], [(x, y)])
                    elif self.grid.data[x, y, 0] == Task.id():
                        self.grid.clear_task_at(x, y)
                        self.cleaned += 1

            new_direction = random.sample(max_smells[1], 1)[0]
            self.move_to(*new_direction)
            self.__place_smells()
            yield self.env.timeout(4)

    def move_to(self, x, y):
        self.grid.data[self.x, self.y, 0] = 0
        self.grid.data[x, y, 0] = Solver.id()
        self.x = x
        self.y = y

    def __place_smells(self):
        for x in xrange(5):
            Smell(self.env, self.x, self.y, self.grid, self.params,
                  smell_dimension=2)

    def __total_smell_value(self, x, y):
        return self.grid.data[x, y, 1] - self.grid.data[x, y, 2]
