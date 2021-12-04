from wrapper import Wrapper

import numpy as np


class Solver(Wrapper):

    def __init__(self, day):
        super(Solver, self).__init__(day=day)
        self.board_size = 5
        self.raw_input = [r for r in self.load_input() if r]
        self.parse_input()

    def parse_input(self):
        self.numbers = [int(x) for x in self.raw_input[0].split(',')]
        self.last_number = None
        self.n_boards = int((len(self.raw_input) - 1) / self.board_size)
        self.boards = [
            np.array([
                row.split() for row in self.raw_input[i * self.board_size + 1
                                                      :i * self.board_size + 6]
            ]).astype(np.int) for i in range(self.n_boards)
        ]
        self.board_masks = [
            np.full((self.board_size, self.board_size), False, bool)
            for _ in range(self.n_boards)
        ]

    def reset(self):
        self.board_masks = [
            np.full((self.board_size, self.board_size), False, bool)
            for _ in range(self.n_boards)
        ]

    def mark_drawn_number(self, x):
        for i_board, board in enumerate(self.boards):
            self.board_masks[i_board] = np.logical_or(self.board_masks[i_board],
                                                      board == x)

    def check_for_winners(self):
        winners = []
        for i_mask, mask in enumerate(self.board_masks):
            if np.any(np.all(mask, axis=0)) or np.any(np.all(mask, axis=1)):
                winners.append(i_mask)
        return winners

    def calculate_answer(self, i_board):
        winning_board = self.boards[i_board]
        final_state = self.board_masks[i_board]
        unmarked_numbers = winning_board[~final_state]
        print(np.sum(unmarked_numbers) * self.last_number)

    def delete_winning_board(self, winners):
        self.boards = [b for i, b in enumerate(self.boards)
                       if i not in winners]
        self.board_masks = [m for i, m in enumerate(self.board_masks)
                            if i not in winners]

    def task1(self):
        for nr in self.numbers:
            self.last_number = nr
            self.mark_drawn_number(nr)
            winners = self.check_for_winners()
            if winners:
                self.calculate_answer(winners[0])
                return True

    def task2(self):
        for nr in self.numbers:
            self.last_number = nr
            self.mark_drawn_number(nr)
            winners = self.check_for_winners()
            if winners:
                if len(self.boards) == 1:
                    self.calculate_answer(0)
                    return True
                self.delete_winning_board(winners)


day4 = Solver('04')
day4.task1()
day4.reset()
day4.task2()