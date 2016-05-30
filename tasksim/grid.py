from collections import defaultdict
import random
from task import Task
from solver import Solver
import numpy as np


class Grid(object):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        # [x][y] = [object_type, smell]
        self.data = np.zeros((self.params.width, self.params.height, 2))
        self.tasks = {}

        for _ in xrange(params.task_count):
            task = self.add_task()
            self.tasks[(task.x, task.y)] = task

        for _ in xrange(params.task_count / 3):
            self.add_solver()

    def idle(self):
        while True:
            idle_time = random.randint(1, 10)
            yield self.env.timeout(idle_time)
            self.generate_task()

    def clear_task_at(self, x, y):
        self.task_at(x, y).clear()

    def task_at(self, x, y):
        return self.tasks[(x, y)]

    def generate_task(self):
        if random.random() < 0.5:
            self.add_task()

    def __find_empty_spot(self):
        x, y = None, None
        while True:
            x = random.randint(0, self.params.width - 1)
            y = random.randint(0, self.params.height - 1)
            if self.data[x, y, 0] == 0:
                break

        return (x, y)

    def add_task(self):
        x, y = self.__find_empty_spot()
        self.data[x, y, 0] = Task.id()
        return Task(self.env, x, y, self, self.params)

    def add_solver(self):
        x, y = self.__find_empty_spot()
        self.data[x, y, 0] = Solver.id()
        Solver(self.env, x, y, self, self.params)
