from PIL import Image
from task import Task
from solver import Solver
import pickle
import os
import time
import matplotlib.pyplot as plt
import json
import numpy as np


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
                solver_data = pickle.load(self.data_file)
                self.__dump_image(grid_data, task_data, step)
                step += 5
            except EOFError:
                break

        self.data_file.close()

    def generate_statistics(self):

        stat_json = {}

        stink_x = []
        stink_y = []
        cleaned_tasks_per_task = []
        cleaned_tasks_per_solver = []
        avg_cleaned_trash_lvl = []

        # save configuration
        stat_json['width'] = self.params.width
        stat_json['height'] = self.params.height
        stat_json['steps'] = self.params.steps
        stat_json['fill_level'] = self.params.fill_level
        stat_json['max_fill_level'] = self.params.max_fill_level
        stat_json['lifepoints'] = self.params.lifepoints
        stat_json['cooldown'] =  self.params.cooldown
        stat_json['task_count'] = self.params.task_count
        stat_json['task_ratio'] = self.params.task_ratio

        # stink level in time
        stat_json['stink_level'] = {}
        
        stat_json['cleaned_by_solvers_in_step'] = {}

        self.data_file.close()
        self.data_file = open("result.dat", "r")
        step = 0
        while True:
            try:
                state = pickle.load(self.data_file)
                _ = pickle.load(self.data_file)
                solver_data = pickle.load(self.data_file)
                stink_level = self.__get_stink_level(state)
                stat_json['stink_level'][step] = stink_level
                stat_json['cleaned_by_solvers_in_step'][step] = solver_data

                stink_x.append(step)
                stink_y.append(stink_level)

                step += 5

            except EOFError:
                break
        self.data_file.close()

        # cleaned tasks (for task)
        stat_json['cleaned_tasks_per_task'] = {}
        task_no = 0
        for _, task in self.grid.tasks.iteritems():
            stat_json['cleaned_tasks_per_task'][task_no] = task.cleaned
            cleaned_tasks_per_task.append(task.cleaned)
            task_no +=1

        # cleaned tasks (for solver)
        stat_json['cleaned_tasks_per_solver'] = {}
        solver_no = 0
        for solver in self.grid.solvers:
            stat_json['cleaned_tasks_per_solver'][solver_no] = solver.cleaned
            cleaned_tasks_per_solver.append(solver.cleaned)
            solver_no +=1

        # avarage level of fill for tasks on clean:
        stat_json['avg_cleaned_trash_lvl'] = {}
        task_no = 0
        for _, task in self.grid.tasks.iteritems():
            avg = task.cleanedFill / float(task.cleaned) if task.cleaned else 0
            stat_json['avg_cleaned_trash_lvl'][task_no] = avg
            avg_cleaned_trash_lvl.append(avg)
            task_no +=1


        # save stats in file
        stat_path = "./stats"
        if not os.path.exists(stat_path):
            os.makedirs(stat_path)

        stat_filename = "stats_{}.json".format(self.timestamp)
        stat_file = open(os.path.join(stat_path, stat_filename), "wb")
        stat_file.write(json.dumps(stat_json))

        stat_file.close()

        # draw plots
        plot_filename = "stink_level_{}.png".format(self.timestamp)
        plt.plot(stink_x, stink_y)
        plt.xlabel('time')
        plt.ylabel('stink level')
        plt.savefig(os.path.join(stat_path, plot_filename))

        plot_filename = "cleaned_tasks_per_task_{}.png".format(self.timestamp)
        ind = np.arange(task_no)
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, cleaned_tasks_per_task, width, color='r')
        ax.set_ylabel('Cleaned tasks')
        ax.set_title('Cleaned tasks per task')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(xrange(task_no))
        ax.set_xlabel('Task')
        plt.savefig(os.path.join(stat_path, plot_filename))

        plot_filename = "cleaned_tasks_per_solver_{}.png".format(self.timestamp)
        ind = np.arange(solver_no)
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, cleaned_tasks_per_solver, width, color='r')
        ax.set_ylabel('Cleaned tasks')
        ax.set_title('Cleaned tasks per solver')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(xrange(solver_no))
        ax.set_xlabel('Solver')
        plt.savefig(os.path.join(stat_path, plot_filename))

        plot_filename = "avg_cleaned_trash_lvl_{}.png".format(self.timestamp)
        ind = np.arange(task_no)
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, avg_cleaned_trash_lvl, width, color='r')
        ax.set_ylabel('Average clean trash level')
        ax.set_title('Average clean trash level per task')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(xrange(task_no))
        ax.set_xlabel('Task')
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
        cleaned_by_solver = [s.cleaned for s in self.grid.solvers]
        avg = sum(cleaned_by_solver) / float(len(cleaned_by_solver))
        solver_data = {'min': min(cleaned_by_solver),
                       'avg': avg,
                       'max': max(cleaned_by_solver)}
        pickle.dump(solver_data, self.data_file, protocol=2)

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
