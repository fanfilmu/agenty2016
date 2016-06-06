from base_strategy import BaseStrategy
from task import Task
import random


class BinsStrategy(BaseStrategy):
    def apply(self):
        max_smells = (-1, [])
        for x in xrange(self.solver.x - 1, self.solver.x + 2):
            for y in range(self.solver.y - 1, self.solver.y + 2):
                if x < 0 or x >= self.solver.params.width:
                    continue
                if y < 0 or y >= self.solver.params.height:
                    continue

                if self.solver.grid.data[x, y, 0] == 0:
                    if self.__total_smell_value(x, y) == max_smells[0]:
                        max_smells[1].append((x, y))
                    elif self.__total_smell_value(x, y) > max_smells[0]:
                        max_smells = (self.solver.grid.data[x, y, 1], [(x, y)])
                elif self.solver.grid.data[x, y, 0] == Task.id():
                    self.solver.grid.clear_task_at(x, y)
                    self.solver.cleaned += 1

        return random.sample(max_smells[1], 1)[0]

    def __total_smell_value(self, x, y):
        return self.solver.grid.data[x, y, 1]
