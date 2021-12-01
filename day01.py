from wrapper import Wrapper


class Solver(Wrapper):

    def __init__(self, day: str):
        super().__init__(day=day)
        self.input = super().load_input_as_int()
        self.example = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    def task1(self, input):
        print(
            sum(input[i + 1] > input[i]
                for i in range(len(input) - 1))
        )

    def task2(self, input):
        print(
            sum(
                sum(input[i:(i + 3)]) < sum(input[(i + 1):(i + 4)])
                for i in range(len(input) - 3)
            )
        )


solver = Solver('01')

solver.task1(solver.example)
solver.task1(solver.input)

solver.task2(solver.example)
solver.task2(solver.input)
