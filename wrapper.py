class Wrapper:

    def __init__(self, day: str, example: bool = False):
        self.day = day
        self.use_example = example

    def load_input(self):
        path = (f'./inputs/input{self.day}.txt' if not self.use_example
                else f'./inputs/input{self.day}_example.txt')
        with open(path) as fp:
            return fp.read().splitlines()

    def load_input_as_int(self):
        return [int(i) for i in self.load_input()]

    def load_input_row_as_int(self):
        return [int(i) for i in self.load_input()[0].split(',')]

    def load_input_as_array(self):
        rows = self.load_input()
        return [[int(i) for i in list(r)] for r in rows]

    def print_input(self):
        print(self.load_input())
