from wrapper import Wrapper

from collections import defaultdict

opening_chars = ('(', '[', '{', '<')
closing_chars = (')', ']', '}', '>')
pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
scores_corrupted = {')': 3, ']': 57, '}': 1197, '>': 25137}
scores_missing = {')': 1, ']': 2, '}': 3, '>': 4}


class Chunk:

    def __init__(self):
        self.opening_char = None
        self.closing_char = None
        self.contains = []

    def print(self):
        print(self.opening_char, end='')
        for ch in self.contains:
            ch.print()
        print(self.closing_char, end='')


class Solver(Wrapper):

    def __init__(self, day, example):
        super(Solver, self).__init__(day, example)
        self.input = self.load_input()
        self.chunks = []
        self.corrupted_chars = []
        self.corrupted_lines = []
        self.missing_chars = defaultdict(str, '')
        for i, line in enumerate(self.input):
            self.parse_line(i, line)

    def parse_line(self, i_line, line, chunk_old=Chunk()):
        while line:
            char = line[0]
            if char in opening_chars:
                chunk_new = Chunk()
                chunk_new.opening_char = char
                if chunk_old is not None:
                    chunk_old.contains.append(chunk_new)
                line = self.parse_line(i_line, line[1:], chunk_new)
            elif char in closing_chars:
                chunk_old.closing_char = char
                if pairs[chunk_old.opening_char] != chunk_old.closing_char:
                    self.corrupted_chars.append(char)
                    self.corrupted_lines.append(i_line)
                    return ''  # Stop the iteration.
                return line[1:]
        if chunk_old.closing_char is None and chunk_old.opening_char is not None:  # Unfinished input.
            self.finish_chunk(chunk_old, i_line)
        else:
            self.chunks.append(chunk_new)

    def finish_chunk(self, chunk, i_line):
        chunk.closing_char = pairs[chunk.opening_char]
        self.missing_chars[i_line] += chunk.closing_char

    def task1(self):
        print(sum(scores_corrupted.get(char, 0) for char in self.corrupted_chars))

    def task2(self):
        scores = []
        for i_line, missing_chars in self.missing_chars.items():
            if i_line in self.corrupted_lines:
                continue
            score = 0
            for missing_char in missing_chars:
                score = 5 * score + scores_missing[missing_char]
            scores.append(score)
        scores_sorted = sorted(scores)
        nr_completed_lines = len(scores_sorted)
        mid_index = int(nr_completed_lines / 2)
        print(scores_sorted[mid_index])


example = False
day10 = Solver('10', example)
day10.task1()
day10.task2()
