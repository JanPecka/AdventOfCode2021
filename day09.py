from functools import reduce
import numpy as np

from wrapper import Wrapper


class Map:

    def __init__(self, map):
        self.heightmap = np.array(map)
        self.i_dim, self.j_dim = self.heightmap.shape
        self.lowest_point = 0
        self.highest_point = 9
        self.risk = 1

    def find_increases_in_direction(self, direction: str):
        if direction == 'right':
            i, ax, padding_indexes = 0, 1, ((0, 0), (0, 1))
        elif direction == 'left':
            i, ax, padding_indexes = -1, 1, ((0, 0), (1, 0))
        elif direction == 'down':
            i, ax, padding_indexes = 0, 0, ((0, 1), (0, 0))
        elif direction == 'up':
            i, ax, padding_indexes = -1, 0, ((1, 0), (0, 0))
        arr_shifted = np.delete(self.heightmap, obj=i, axis=ax)
        arr_padded = np.pad(arr_shifted, padding_indexes,
                            constant_values=self.highest_point + 1)
        increases = (self.heightmap - arr_padded) < 0
        return increases

    def find_local_minima(self):
        one_dim_minima = [self.find_increases_in_direction(dir)
                          for dir in ('right', 'left', 'down', 'up')]
        local_minima = reduce(lambda a, b: np.logical_and(a, b), one_dim_minima)
        return local_minima

    def get_risk_at_local_minimas(self):
        local_minima = self.find_local_minima()
        local_minima_vals = self.heightmap[local_minima]
        local_minima_risk = local_minima_vals + 1
        print(sum(local_minima_risk))

    def move(self, i, j, direction):
        if direction == 'down':
            i += 1
        elif direction == 'up':
            i -= 1
        elif direction == 'right':
            j += 1
        elif direction == 'left':
            j -= 1
        return i, j

    def move_upward_from_position(self, i, j, visited_positions, basin_size):
        for dir in ('left', 'right', 'up', 'down'):
            increases = self.find_increases_in_direction(dir)
            if increases[i, j]:
                i_new, j_new = self.move(i, j, dir)
                if (i_new, j_new) in visited_positions:
                    continue
                elif i_new < 0 or j_new < 0 or i_new > self.i_dim - 1 or j_new > self.j_dim - 1:  # OOB
                    continue
                elif self.heightmap[i_new, j_new] == 9: # Basin border
                    continue
                else:
                    basin_size += 1
                    visited_positions.add((i_new, j_new))
                    visited_positions, basin_size = (
                        self.move_upward_from_position(i_new, j_new, visited_positions, basin_size)
                    )
        return visited_positions, basin_size

    def explore_basins(self):
        local_minima = self.find_local_minima()
        local_minima_indexes = np.transpose(local_minima.nonzero())
        basin_sizes = []
        for i_min, minima in enumerate(local_minima_indexes):
            print(f"Minima {i_min} out of {len(local_minima_indexes)}.")
            i, j = minima
            visited_positions = {(i, j)}
            basin_size = 1
            _, basin_size = self.move_upward_from_position(i, j, visited_positions, basin_size)
            basin_sizes.append(basin_size)
        return basin_sizes


class Solver(Wrapper):

    def __init__(self, day, example):
        super(Solver, self).__init__(day, example)
        input_raw = self.load_input_as_array()
        self.map = Map(input_raw)

    def task1(self):
        self.map.get_risk_at_local_minimas()

    def task2(self):
        basin_sizes = self.map.explore_basins()
        largest_basins = sorted(basin_sizes, reverse=True)[:3]
        print(reduce(lambda x, y: x * y, largest_basins))


"""
Possible improvements:
    - create a class for exploring basins -> better readability.
    - the `find_increases_in_direction` detects increases at every position, which is way too redundant for its use
      in task #2
"""

day9 = Solver('09', False)
day9.task1()
day9.task2()
