import argparse
import json


class Params(object):
    def __init__(self):
        self.fill_level = 1
        self.max_fill_level = 10
        self.width = 1024
        self.height = 1024

    def parse(self):
        args = self.__parser().parse_args()
        self.fill_level = args.fill_level
        self.max_fill_level = args.max_fill_level
        self.width = args.width
        self.height = args.height

    def __parser(self):
        parser = argparse.ArgumentParser(
            description='Simulation of locating and solving randomly placed'
                        ' tasks on 2D plane')
        parser.add_argument('--fill-level', dest='fill_level',
                            type=int, default=1,
                            help='Initial fill level for new bins - determines'
                                 ' how quickly new smells are generated.'
                                 ' Defaults to 1')
        parser.add_argument('--max-fill-level', dest='max_fill_level',
                            type=int, default=10,
                            help='Maximal fill level for bins - determines'
                                 ' highest possible value for fill_level.'
                                 ' Defaults to 10')

        parser.add_argument('--width', dest='width', type=int, default=1024,
                            help='Width of the plane. Defaults to 1024')

        parser.add_argument('--height', dest='height', type=int, default=1024,
                            help='Height of the plane. Defaults to 1024')

        return parser
