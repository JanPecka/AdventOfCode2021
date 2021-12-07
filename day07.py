from wrapper import Wrapper

from numpy import median, mean


class Solver(Wrapper):

    def __init__(self, day, example=False):
        super(Solver, self).__init__(day)
        if example:
            self.positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        else:
            self.positions = super().load_input_row_as_int()

    def task1(self):
        final_position = median(self.positions)
        print(f'Final position: {final_position}')
        fuel_needed = sum(abs(pos - final_position) for pos in self.positions)
        print(f'Fuel needed: {fuel_needed}')

    def task2(self):
        final_position = int(mean(self.positions))
        print(f'Final position: {final_position}')
        fuel_needed = sum(
            sum(range(1, abs(pos - final_position) + 1))
            for pos in self.positions
        )
        print(f'Fuel needed: {fuel_needed}')


example = False
day7 = Solver('07', example)
day7.task1()
day7.task2()
