from base_strategy import BaseStrategy
import random
from task import Task


class RandomStrategy(BaseStrategy):
    def apply(self):
        x = min(self.solver.params.width - 1, max(0, random.randint(self.solver.x - 1, self.solver.x + 1)))
        y = min(self.solver.params.height - 1, max(0, random.randint(self.solver.y - 1, self.solver.y + 1)))

        if self.solver.grid.data[x, y, 0] == Task.id():
            self.solver.grid.clear_task_at(x, y)
            self.solver.cleaned += 1

        return (x, y)
