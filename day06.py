from wrapper import Wrapper
from collections import Counter

class Solver(Wrapper):

    def __init__(self, day):
        super().__init__(day)
        # self.fish = [3, 4, 3, 1, 2]
        self.fish = super().load_input_row_as_int()

        self.new_fish = 8
        self.restart = 6
        self.fish_in_labor = -1

        self.fish = Counter(self.fish)

    def pass_one_day(self, fish):

        def age(f):
            return Counter({
                (age - 1): f[age] for age in range(self.fish_in_labor + 1,
                                                   self.new_fish + 1)
            })

        def reset(f):
            n_reset = f[self.fish_in_labor]
            f[self.restart] += n_reset
            f[self.fish_in_labor] = 0
            return f

        def newborns(f):
            n_new = f[self.fish_in_labor]
            f[self.new_fish] = n_new
            return f


        aged_fish = age(fish)
        new_fish = newborns(aged_fish)
        restarted_fish = reset(new_fish)

        return restarted_fish

    def task1(self, n_days: int):
        for day in range(n_days):
            self.fish = self.pass_one_day(self.fish)

        print(sum(t[1] for t in self.fish.items()))


day6 = Solver('06')
day6.task1(256)