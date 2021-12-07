from wrapper import Wrapper

import numpy as np


class Line:

    def __init__(self, start: str, end: str):
        self.x1, self.y1 = (int(i) for i in start.split(','))
        self.x2, self.y2 = (int(i) for i in end.split(','))

    def is_diagonal(self):
        return not (self.x1 == self.x2 or self.y1 == self.y2)


class Map:

    x_max = 1000
    y_max = 1000

    def __init__(self):
        self.crosses = np.zeros((self.x_max, self.y_max), dtype=int)

    def draw_line(self, line: Line):
        x_dir = 1 if line.x2 >= line.x1 else -1
        y_dir = 1 if line.y2 >= line.y1 else -1
        self.crosses[
            range(line.x1, line.x2 + x_dir, x_dir),
            range(line.y1, line.y2 + y_dir, y_dir)
        ] += 1

    def count_crosses(self):
        return sum(sum(self.crosses > 1))


class Solver(Wrapper):

    def __init__(self, day):
        super(Solver, self).__init__(day)
        lines_raw = super(Solver, self).load_input()
        # lines_raw = "0,9 -> 5,9 X 8,0 -> 0,8 X 9,4 -> 3,4 X 2,2 -> 2,1 X " \
        #             "7,0 -> 7,4 X 6,4 -> 2,0 X 0,9 -> 2,9 X 3,4 -> 1,4 X " \
        #             "0,0 -> 8,8 X 5,5 -> 8,2".split(' X ')
        self.lines = [r.split(' -> ') for r in lines_raw]

    def task1(self):
        map = Map()
        for line in self.lines:
            line = Line(*line)
            if line.is_diagonal():
                continue
            map.draw_line(line)
        print(map.count_crosses())

    def task2(self):
        map = Map()
        for line in self.lines:
            line = Line(*line)
            map.draw_line(line)
        print(map.count_crosses())


solver = Solver('05')
solver.task1()
solver.task2()
