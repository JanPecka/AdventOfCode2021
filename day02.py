from wrapper import Wrapper


class Solver(Wrapper):

    def __init__(self, day: str):
        super().__init__(day=day)
        self.example = [
            "forward 5",
            "down 5",
            "forward 8",
            "up 3",
            "down 8",
            "forward 2",
        ]
        self.instructions = self.load_input()
        self.distance = 0
        self.depth = 0
        self.aim = 0

    def reset_location(self):
        self.distance = self.depth = self.aim = 0

    def move_1(self, direction, value):
        value = int(value)
        if direction == 'forward':
            self.distance += value
        elif direction == 'down':
            self.depth += value
        elif direction == 'up':
            self.depth -= value
        else:
            raise ValueError('Wrong direction type.')

    def move_2(self, direction, value):
        value = int(value)
        if direction == 'forward':
            self.distance += value
            self.depth += self.aim * value
        elif direction == 'down':
            self.aim += value
        elif direction == 'up':
            self.aim -= value
        else:
            raise ValueError('Wrong direction type.')

    def task1(self):
        for instruction in self.instructions:
            self.move_1(*instruction.split(' '))

        print(self.distance * self.depth)

    def task2(self):
        for instruction in self.instructions:
            self.move_2(*instruction.split(' '))

        print(self.distance * self.depth)



day2 = Solver('02')
day2.task1()
day2.reset_location()
day2.task2()
