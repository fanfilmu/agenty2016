from PIL import Image
import os
import copy


class Snapshot(object):
    def __init__(self, env, grid, params):
        self.env = env
        self.grid = grid
        self.params = params
        self.env.process(self.capture())

    def capture(self):
        while True:
            current = self.grid.data.copy()
            newpid = os.fork()
            if newpid == 0:
                img = Image.new('RGB', (self.params.width, self.params.height))

                data = []
                for y in xrange(self.params.height):
                    for x in xrange(self.params.width):
                        data.append(self.__parse_cell(current[x, y, 0]))

                print 'saving image'
                img.putdata(data)
                img.save('sim%d.png' % self.env.now)
            else:
                yield self.env.timeout(5)

    def __parse_cell(self, cell):
        if cell >= 1e100:
            return (255, 234, 4)
        else:
            v = min(255, cell)
            return (v, v, v)
