import random


class Smell(object):
    def __init__(self, env, x, y, grid, params, smell_dimension=1):
        self.env = env
        self.x = x
        self.y = y
        self.grid = grid
        self.grid.data[x, y, 1] += 1
        self.params = params
        self.lifepoints = params.lifepoints
        self.smell_dimension = smell_dimension
        self.env.process(self.move())

    def move(self):
        while self.lifepoints > 0:
            min_smells = (1e100, [])
            for x in xrange(self.x - 1, self.x + 2):
                for y in range(self.y - 1, self.y + 2):
                    if x < 0 or x >= self.params.width:
                        continue
                    if y < 0 or y >= self.params.height:
                        continue

                    if self.grid.data[x, y, 1] == min_smells[0]:
                        min_smells[1].append((x, y))
                    elif self.grid.data[x, y, 1] < min_smells[0]:
                        min_smells = (self.grid.data[x, y, 1], [(x, y)])

            new_direction = random.sample(min_smells[1], 1)[0]
            self.move_to(*new_direction)
            yield self.env.timeout(4)

        self.grid.data[self.x, self.y, 1] -= 1

    def move_to(self, x, y):
        self.grid.data[self.x, self.y, 1] -= 1
        self.grid.data[x, y, 1] += 1
        self.x = x
        self.y = y
        self.lifepoints -= 1
