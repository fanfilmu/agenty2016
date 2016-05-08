from collections import defaultdict
import random
from task import Task


class Grid(object):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.data = defaultdict(lambda: 0)
        self.env.process(self.idle())

        self.add_task()
        self.add_task()
        self.add_task()
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
            if self.data[x, y, 0] < 1e100:
                break
        self.data[x, y, 0] = 1e100
        Task(self.env, x, y, self, self.params)
