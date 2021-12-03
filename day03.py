from wrapper import Wrapper


class Solver(Wrapper):

    def __init__(self, day):
        super().__init__(day=day)
        self.example = [
            "00100",
            "11110",
            "10110",
            "10111",
            "10101",
            "01111",
            "00111",
            "11100",
            "10000",
            "11001",
            "00010",
            "01010",
            ]
        self.input = self.load_input()

    def extract_position(self, i_pos, input):
        return [w[i_pos] for w in input]

    def find_most_common_bit(self, word):
        n_ones = sum([int(i) for i in word])
        return '1' if n_ones >= (len(word) / 2) else '0'

    def calculate_gamma_and_epsilon(self, most_common_bits):
        gamma = ''.join(i for i in most_common_bits)
        epsilon = ''.join(str(1 - int(i)) for i in most_common_bits)
        return gamma, epsilon

    def task1(self, example=False):
        input = self.example if example else self.input
        n_pos = len(input[0])
        positions = [self.extract_position(i, input) for i in range(n_pos)]
        most_common_bits = [self.find_most_common_bit(w) for w in positions]
        gamma, epsilon = self.calculate_gamma_and_epsilon(most_common_bits)
        print(int(gamma, 2) * int(epsilon, 2))

    def filter_out(self, i_pos, bit, candidates):
        new_candidates = [c for c in candidates if c[i_pos] == str(bit)]
        return new_candidates

    def task2(self, example=False):
        candidates_1 = self.example if example else self.input
        candidates_2 = self.example if example else self.input
        for i_pos in range(len(candidates_1[0])):
            word_1 = self.extract_position(i_pos, candidates_1)
            word_2 = self.extract_position(i_pos, candidates_2)
            most_common_bit_1 = self.find_most_common_bit(word_1)
            most_common_bit_2 = '1' if self.find_most_common_bit(word_2) == '0' else '0'
            if len(candidates_1) > 1:
                candidates_1 = self.filter_out(i_pos, most_common_bit_1, candidates_1)
            if len(candidates_2) > 1:
                candidates_2 = self.filter_out(i_pos, most_common_bit_2, candidates_2)
        print(int(candidates_1[0], 2) * int(candidates_2[0], 2))



day3 = Solver('03')
day3.task1()
day3.task2()