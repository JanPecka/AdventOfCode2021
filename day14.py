from wrapper import Wrapper

from collections import defaultdict


class Polymer:

    def __init__(self, template, rules):

        def count_pairs(template):
            pairs = defaultdict(int)
            for i in range(len(template) - 1):
                pair = template[i:i + 2]
                pairs[pair] += 1
            return pairs

        self.init_template = template
        self.rules = rules
        self.pairs = count_pairs(template)

    def grow(self):
        pairs = [(pair, count) for pair, count in self.pairs.items()]
        for pair, count in pairs:
            assert pair in self.rules, f'No rule for pair {pair}.'
            self.pairs[pair] -= count
            self.pairs[f'{pair[0]}{self.rules[pair]}'] += count
            self.pairs[f'{self.rules[pair]}{pair[1]}'] += count

    def find_least_and_most_common_letter(self):
        present_pairs = [(pair, count) for pair, count in self.pairs.items() if count > 0]
        counts = defaultdict(int)
        for pair, count in present_pairs:
            for letter in pair:
                counts[letter] += .5 * count  # Duplication of letters in pairs
        counts[self.init_template[0]] += .5  # First and last letter are not duplicated.
        counts[self.init_template[-1]] += .5
        counts_sorted = sorted([(letter, count) for letter, count in counts.items()],
                               key=lambda t: t[1])
        return counts_sorted[0], counts_sorted[-1]


class Solver(Wrapper):

    def __init__(self, day, example):

        def parse_input(input):
            template = input[0]
            rules = {}
            for line in input[2:]:
                pair, letter = line.split(' -> ')
                rules[pair] = letter
            return template, rules

        super(Solver, self).__init__(day, example)
        input = self.load_input()
        self.polymer = Polymer(*parse_input(input))

    def iterate(self, n_iter):
        for i_iter in range(n_iter):
            self.polymer.grow()
        least_common, most_common = self.polymer.find_least_and_most_common_letter()
        print(most_common[1] - least_common[1])


example = False
day14 = Solver('14', example)
day14.iterate(40)
