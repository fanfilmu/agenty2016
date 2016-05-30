import argparse
import json


class Params(object):
    def __init__(self):
        self.fill_level = 1
        self.max_fill_level = 10
        self.width = 1024
        self.height = 1024
        self.lifepoints = 15
        self.task_count = 10
        self.steps = 1000

    def parse(self):
        args = self.__parser().parse_args()
        self.fill_level = args.fill_level
        self.max_fill_level = args.max_fill_level
        self.width = args.width
        self.height = args.height
        self.lifepoints = args.lifepoints
        self.task_count = args.task_count
        self.steps = args.steps

    def __parser(self):
        parser = argparse.ArgumentParser(
            description='Simulation of locating and solving randomly placed'
                        ' tasks on 2D plane',
            fromfile_prefix_chars='@')
        parser.add_argument('-F', '--fill-level', dest='fill_level',
                            type=int, default=1,
                            help='Initial fill level for new bins - determines'
                                 ' how quickly new smells are generated.'
                                 ' Defaults to 1')
        parser.add_argument('-M', '--max-fill-level', dest='max_fill_level',
                            type=int, default=10,
                            help='Maximal fill level for bins - determines'
                                 ' highest possible value for fill_level.'
                                 ' Defaults to 10')

        parser.add_argument('-W', '--width', dest='width', type=int, default=1024,
                            help='Width of the plane. Defaults to 1024')

        parser.add_argument('-H', '--height', dest='height', type=int, default=1024,
                            help='Height of the plane. Defaults to 1024')

        parser.add_argument('-L', '--lifepoints', dest='lifepoints', type=int,
                            default=15, help='Lifepoints of a new smell.'
                            ' Defaults to 15')

        parser.add_argument('-T', '--task-count', dest='task_count', type=int,
                            default=10, help='Amount of task generating '
                            'smells. Defaults to 10')

        parser.add_argument('-S', '--steps', dest='steps', type=int,
                            default=10, help='Maximum amount of simulation '
                            'steps. Defaults to 1000')

        return parser
