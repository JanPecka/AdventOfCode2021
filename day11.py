from wrapper import Wrapper

import numpy as np

energy_increase = 1
reset_energy_level = 0
flash_point = 10


class Octopus:

    def __init__(self, energy, position_in_swarm):
        self.energy_level = energy
        self.position = position_in_swarm
        self.ready_to_flash = self.is_ready_to_flash()
        self.flashed = False
        self.n_flashes = 0

    def increase_energy(self, diff=energy_increase):
        self.energy_level += diff
        self.ready_to_flash = self.is_ready_to_flash()

    def is_ready_to_flash(self):
        return self.energy_level >= flash_point

    def reset(self):
        if self.flashed:
            self.energy_level = reset_energy_level
            self.flashed = False
            self.ready_to_flash = False

    def flash(self):
        self.flashed = True
        self.n_flashes += 1

    def get_neighbours(self, swarm):
        mask = np.zeros(swarm.shape, dtype=bool)
        r = self.position[0]
        c = self.position[1]
        mask[r - 1 if r != 0 else r:r + 2, c - 1 if c != 0 else c: c + 2] = True
        mask[r, c] = False
        return swarm[mask]


class Swarm:

    def __init__(self, map):
        self.swarm = np.array(
            [[Octopus(en, (i_row, i_col)) for i_col, en in enumerate(row)]
             for i_row, row in enumerate(map)]
        )

    def increase_swarm_energy(self):
        for octo in self.swarm.flat:
            octo.increase_energy()

    def get_octos_ready_to_flash(self):
        return [octo for octo in self.swarm.flat if octo.ready_to_flash and not octo.flashed]

    def swarm_flash(self):
        octos_to_flash = self.get_octos_ready_to_flash()
        while octos_to_flash:
            octo = octos_to_flash[0]
            octo.flash()
            neighbours = octo.get_neighbours(self.swarm)
            for octo_n in neighbours.flat:
                octo_n.increase_energy()
            octos_to_flash = self.get_octos_ready_to_flash()

    def reset(self):
        for octo in self.swarm.flat:
            octo.reset()

    def print(self):
        arr_to_print = np.array([[octo.energy_level for octo in row] for row in self.swarm])
        print(arr_to_print)

    def count_flashes(self):
        return sum(octo.n_flashes for octo in self.swarm.flat)

    def did_all_octos_flash(self):
        swarm_flashes = np.array([[octo.flashed for octo in row] for row in self.swarm])
        return np.all(swarm_flashes)


class Solver(Wrapper):

    def __init__(self, day, example):
        super(Solver, self).__init__(day, example)
        input_raw = self.load_input_as_array()
        self.swarm = Swarm(input_raw)

    def one_iteration(self):
        self.swarm.increase_swarm_energy()
        self.swarm.swarm_flash()
        res = 0
        if self.swarm.did_all_octos_flash():
            res = 1
        self.swarm.reset()
        return res

    def iterate(self, n_iter):
        for i_iter in range(n_iter):
            all_flashed = self.one_iteration() == 1
            if all_flashed:
                print(f"All the octos flashed at iteration {i_iter + 1}.")
        print(f"Iteration {i_iter + 1}, number of flashes {self.swarm.count_flashes()}")


example = False
day11 = Solver('11', example)
day11.iterate(400)