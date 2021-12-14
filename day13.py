from wrapper import Wrapper

import numpy as np


class Paper:

    def __init__(self, indexes_w_dots):
        y_indexes = [i[0] for i in indexes_w_dots]
        x_indexes = [i[1] for i in indexes_w_dots]
        shape = max(x_indexes) + 1, max(y_indexes) + 1
        paper = np.full(shape, False)
        paper[x_indexes, y_indexes] = True
        self.paper_orig = paper
        self.paper_folded = paper
        # print(paper)

    def count_the_dots(self):
        return self.paper_folded.sum()

    def fold(self, axis, index):
        paper = self.paper_folded
        if axis == 'y':
            assert index == int(paper.shape[0] / 2), "Do you really want me to fold here, it's not in the middle?!"
            assert paper[index].sum() == 0, "There's a dot on the line!"
            upper_half, bottom_half = np.split(paper[[i for i in range(paper.shape[0]) if i != index], :], 2, 0)
            self.paper_folded = np.logical_or(upper_half, np.flip(bottom_half, 0))
        elif axis == 'x':
            assert index == int(paper.shape[1] / 2), "Do you really want me to fold here, it's not in the middle?!"
            assert paper[:, index].sum() == 0, "There's a dot on the line!"
            left_half, right_half = np.split(paper[:, [i for i in range(paper.shape[1]) if i != index]], 2, 1)
            self.paper_folded = np.logical_or(left_half, np.flip(right_half, 1))


class Solver(Wrapper):

    def __init__(self, day, example):
        super(Solver, self).__init__(day, example)
        input_lines = self.load_input()
        self.indexes = []
        self.instructions = []
        for line in input_lines:
            if ',' in line:  # Indexes of dots.
                self.indexes.append([int(i) for i in line.split(',')])
            elif not line:
                continue  # Empty line.
            elif '=' in line:
                instruction = line[11:]
                axis, index = instruction.split('=')
                self.instructions.append([axis, index])

        self.paper = Paper(self.indexes)

    def fold_the_paper(self):
        # print(self.paper.paper_folded)
        for instruction in self.instructions:
            print()
            print(instruction)
            self.paper.fold(instruction[0], int(instruction[1]))
            # print(self.paper.paper_folded)
        pass


example = False
day13 = Solver('13', example)
day13.fold_the_paper()
