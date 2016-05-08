from smell import Smell


class Task(object):
    def __init__(self, env, x, y, grid, params):
        self.env = env
        self.x = x
        self.y = y
        self.grid = grid
        self.params = params
        self.fill = params.fill_level
        self.env.process(self.idle())

    def idle(self):
        while True:
            yield self.env.timeout(3)
            for i in xrange(0, self.fill * 50):
                self.generate_smell()
            self.fill = min(self.params.max_fill_level, self.fill + 1)

    def generate_smell(self):
        Smell(self.env, self.x, self.y, self.grid, self.params)
