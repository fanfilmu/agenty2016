from smell import Smell


class Task(object):
    def __init__(self, env, x, y, grid, params):
        self.env = env
        self.x = x
        self.y = y
        self.grid = grid
        self.params = params
        self.fill = params.fill_level
        self.cleaned = 0
        self.cleanedFill = 0
        self.env.process(self.idle())

    @staticmethod
    def id():
        return 1

    def idle(self):
        while True:
            yield self.env.timeout(3)
            if self.fill >= 0:
                for i in xrange(0, self.fill * 50):
                    self.generate_smell()

            self.fill = min(self.params.max_fill_level, self.fill + 1)

    def clear(self):
        self.cleanedFill += self.fill
        self.fill = self.params.cooldown
        self.cleaned += 1

    def generate_smell(self):
        Smell(self.env, self.x, self.y, self.grid, self.params)
