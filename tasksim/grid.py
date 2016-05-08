from collections import defaultdict
import random
from task import Task
import numpy as np


class Grid(object):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        # [x][y] = [object_type, smell]
        self.data = np.zeros((self.params.width, self.params.height, 2))

        for _ in xrange(params.task_count):
            self.add_task()

    def idle(self):
        while True:
            idle_time = random.randint(1, 10)
            yield self.env.timeout(idle_time)
            self.generate_task()

    def generate_task(self):
        if random.random() < 0.5:
            self.add_task()

    def add_task(self):
        x, y = None, None
        while True:
            x = random.randint(0, self.params.width)
            y = random.randint(0, self.params.height)
            if self.data[x, y, 0] == 0:
                break

        self.data[x, y, 0] = Task.id()
        Task(self.env, x, y, self, self.params)
