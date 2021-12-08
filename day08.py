from wrapper import Wrapper
from collections import Counter, defaultdict

segment_counts = {  # How many times is a segment turned on in all 7 numbers?
    1: 8,
    2: 6,
    3: 8,
    4: 7,
    5: 4,
    6: 9,
    7: 7,
}
number_to_segments = {  # Which segments are turned on for which number.
    0: [1, 2, 3, 5, 6, 7],
    1: [3, 6],
    2: [1, 3, 4, 5, 7],
    3: [1, 3, 4, 6, 7],
    4: [2, 3, 4, 6],
    5: [1, 2, 4, 6, 7],
    6: [1, 2, 4, 5, 6, 7],
    7: [1, 3, 6],
    8: [1, 2, 3, 4, 5, 6, 7],
    9: [1, 2, 3, 4, 6, 7],
}


class Digit:

    def __init__(self, output_encoded: str):
        self.output_encoded = output_encoded
        self.letters = list(output_encoded)
        self.n_segments_on = len(output_encoded)

    def has_unique_nr_of_segments(self):
        return self.n_segments_on in [2, 3, 4, 7]

    def determine_number(self, letter_to_segment):
        segments = sorted(letter_to_segment[lett] for lett in self.letters)
        for nr, segs in number_to_segments.items():
            if segments == segs:
                self.number = nr
                return nr


class Display:

    def __init__(self, instructions_raw: str):
        patterns, digits_encoded = instructions_raw.split(' | ')
        self.patterns = patterns.split()
        self.digits = [Digit(d) for d in digits_encoded.split()]

    def count_segment_occurrences(self):
        """Returns a dict like {nr_occurrences: [letters]}."""
        letter_to_counts =  Counter(''.join(self.patterns))
        count_to_letters = defaultdict(list, [])
        for letter, count in letter_to_counts.items():
            count_to_letters[count].append(letter)
        return count_to_letters

    def get_pattern_lengths(self):
        patterns_to_lengths = {patt: len(patt) for patt in self.patterns}
        lengths_to_patterns = defaultdict(list, [])
        for pattern, length in patterns_to_lengths.items():
            lengths_to_patterns[length].append(pattern)
        return lengths_to_patterns

    def determine_segment_mapping(self):
        count_to_letters = self.count_segment_occurrences()
        lengths_to_patterns = self.get_pattern_lengths()

        segment_mapping = {  # These segments are determined by the number of times they show up among all the digits.
            2: count_to_letters[6][0],
            5: count_to_letters[4][0],
            6: count_to_letters[9][0],
        }
        segment_mapping[1] = (
            list(set(lengths_to_patterns[3][0]) - set(lengths_to_patterns[2][0]))[0]
        )
        segment_mapping[3] = (
            list(set(lengths_to_patterns[2][0]) - {segment_mapping[6]})[0]
        )
        segment_mapping[4] = (
            list((set(lengths_to_patterns[4][0])
             - {segment_mapping[2], segment_mapping[3], segment_mapping[6]}))[0]
        )
        segment_mapping[7] = (
            list((set(lengths_to_patterns[7][0])
             - {letter for letter in segment_mapping.values()}))[0]
        )
        self.letter_to_segment = {seg: lett for lett, seg in segment_mapping.items()}

    def read_digits(self):
        self.determine_segment_mapping()
        return [d.determine_number(self.letter_to_segment) for d in self.digits]



class Solver(Wrapper):

    def __init__(self, day, example):
        super(Solver, self).__init__(day, example)
        self.input_raw = self.load_input()

    def task1(self):
        nr_unique_digits = 0
        for instruction in self.input_raw:
            display = Display(instruction)
            nr_unique_digits += (
                sum(int(digit.has_unique_nr_of_segments()) for digit in display.digits)
            )
        print(nr_unique_digits)

    def task2(self):
        res = 0
        for instruction in self.input_raw:
            display = Display(instruction)
            numbers = display.read_digits()
            res += (sum(n * o for n, o in zip(numbers, (1000, 100, 10, 1))))
        print(res)


day8 = Solver('08', False)
day8.task1()
day8.task2()
