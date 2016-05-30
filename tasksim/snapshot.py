from PIL import Image
from task import Task
from solver import Solver
import pickle
import os


class Snapshot(object):
    def __init__(self, env, grid, params):
        self.env = env
        self.grid = grid
        self.params = params
        self.env.process(self.capture())
        self.data_file = open("result.dat", "wb")

    def capture(self):
        while True:
            print "Dumping at %d" % self.env.now
            self.__dump_pickle()
            yield self.env.timeout(5)

    def generate_images(self):
        self.data_file.close()
        self.data_file = open("result.dat", "r")
        step = 0

        while True:
            try:
                grid_data = pickle.load(self.data_file)
                task_data = pickle.load(self.data_file)
                self.__dump_image(grid_data, task_data, step)
                step += 5
            except EOFError:
                break

        self.data_file.close()

    def __dump_pickle(self):
        pickle.dump(self.grid.data, self.data_file, protocol=2)
        task_data = { k: v.fill for k, v in self.grid.tasks.iteritems() }
        pickle.dump(task_data, self.data_file, protocol=2)

    def __dump_image(self, data, task_data, step):
        img = Image.new('RGB', (self.params.width, self.params.height))
        imgdata = []

        for y in xrange(self.params.height):
            for x in xrange(self.params.width):
                imgdata.append(self.__parse_cell(data, task_data, x, y))

        img.putdata(imgdata)
        img.save('sim%06d.png' % step)

    def __parse_cell(self, data, task_data, x, y):
        cell = data[x][y]

        if cell[0] == Task.id():
            if task_data[(x, y)] > 0:
                return (255, 234, 4)
            else:
                return (4, 255, 34)
        elif cell[0] == Solver.id():
            return (255, 16, 4)
        else:
            v = min(255, int(cell[1]))
            return (v, v, v)
