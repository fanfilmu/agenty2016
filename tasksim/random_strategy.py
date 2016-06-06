from base_strategy import BaseStrategy
import random


class RandomStrategy(BaseStrategy):
    def apply(self):
        x = min(self.solver.params.width, max(0, random.randint(self.solver.x - 1, self.solver.x + 1)))
        y = min(self.solver.params.height, max(0, random.randint(self.solver.x - 1, self.solver.x + 1)))

        if self.solver.grid.data[x, y, 0] == Task.id():
            self.solver.grid.clear_task_at(x, y)
            self.solver.cleaned += 1

        return (x, y)
