from PIL import Image
from task import Task
from solver import Solver
import pickle
import os
import time
import matplotlib.pyplot as plt


class Snapshot(object):
    def __init__(self, env, grid, params):
        self.env = env
        self.grid = grid
        self.params = params
        self.timestamp = time.strftime("%Y_%m_%d_%H%M%S")
        self.images_path = "./images_{}".format(self.timestamp)
        self.env.process(self.capture())
        self.data_file = open("result.dat", "wb")

    def capture(self):
        while True:
            print "Dumping at %d" % self.env.now
            self.__dump_pickle()
            yield self.env.timeout(5)

    def generate_images(self):
        if not os.path.exists(self.images_path):
            os.makedirs(self.images_path)

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

    def generate_statistics(self):

        stink_x = []
        stink_y = []

        stat_path = "./stats"
        if not os.path.exists(stat_path):
            os.makedirs(stat_path)

        stat_filename = "stats_{}.txt".format(self.timestamp)
        stat_file = open(os.path.join(stat_path, stat_filename), "wb")

        # save configuration
        stat_file.write("width: {}\n".format(self.params.width))
        stat_file.write("height: {}\n".format(self.params.height))
        stat_file.write("fill_level: {}\n".format(self.params.fill_level))
        stat_file.write("max_fill_level: {}\n".format(self.params.max_fill_level))
        stat_file.write("lifepoints: {}\n".format(self.params.lifepoints))
        stat_file.write("task_count: {}\n".format(self.params.task_count))

        # stink level in time
        stat_file.write("\n\nstink level:\n")
        self.data_file.close()
        self.data_file = open("result.dat", "r")
        step = 0
        while True:
            try:
                state = pickle.load(self.data_file)
                stink_level = self.__get_stink_level(state)
                stat_file.write("{} {}\n".format(step, stink_level))

                stink_x.append(step)
                stink_y.append(stink_level)

                step += 5

            except EOFError:
                break
        self.data_file.close()

        # cleaned tasks (for task)
        stat_file.write("\n\ntasks done (for task):\n")
        for _, task in self.grid.tasks.iteritems():
            stat_file.write("{}\n".format(task.cleaned))

        # cleaned tasks (for solver)
        stat_file.write("\n\ntasks done (for solver):\n")
        for solver in self.grid.solvers:
            stat_file.write("{}\n".format(solver.cleaned))

        # avarage level of fill for tasks on clean:
        stat_file.write("\n\navarage level of fill on clean:\n")
        for _, task in self.grid.tasks.iteritems():
            avg = task.cleanedFill / float(task.cleaned) if task.cleaned else 0
            stat_file.write("{}\n".format(avg))


        stat_file.close()

        # draw plots
        plot_filename = "stink_level_{}.png".format(self.timestamp)
        plt.plot(stink_x, stink_y)
        plt.xlabel('time')
        plt.ylabel('stink level')
        plt.savefig(os.path.join(stat_path, plot_filename))

        pass

    def __get_stink_level(self, data):

        stink_level = 0
        for y in xrange(self.params.height):
            for x in xrange(self.params.width):
                stink_level += min(255, int(data[x][y][1]))
        return stink_level


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
        img.save(os.path.join(self.images_path, 'sim%d.png' % step))

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
