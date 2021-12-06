class Wrapper:

    def __init__(self, day: str):
        self.day = day

    def load_input(self):
        path = f'./inputs/input{self.day}.txt'
        with open(path) as fp:
            return fp.read().splitlines()

    def load_input_as_int(self):
        return [int(i) for i in self.load_input()]

    def load_input_row_as_int(self):
        return [int(i) for i in self.load_input()[0].split(',')]

    def print_input(self):
        print(self.load_input())
