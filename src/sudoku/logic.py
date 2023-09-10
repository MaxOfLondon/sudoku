# -*- coding: utf-8
import copy
import random
from typing import List, Tuple


class Logic:
    def is_game_over(self, inputs: List[int], solution: List[int]) -> bool:
        if 0 in inputs:
            return False
        return inputs == solution

    def create_game(self, difficulty_percent: int = 50) \
            -> Tuple[List[int], List[int]]:
        solution = self._create_solution()
        puzzle = self._create_puzzle(solution, difficulty_percent)
        return solution, puzzle

    def _create_solution(self) -> List[List[int]]:
        base = 3
        side = base * base

        # pattern for a baseline valid solution
        def pattern(row, col):
            return (base * (row % base) + row // base + col) % side

        # randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s):
            return random.sample(s, len(s))

        source = range(base)
        rows = [
            group * base + row for group in shuffle(source)
            for row in shuffle(source)
        ]
        cols = [
            group * base + col for group in shuffle(source)
            for col in shuffle(source)
        ]
        nums = shuffle(range(1, base * base + 1))

        # produce board using randomized baseline pattern
        return [
            [nums[pattern(row, col)] for col in cols]
            for row in rows
        ]

    def _create_puzzle(self, solution, difficulty_percent):
        def scaled_clamp(value, from1, to1, from2, to2):
            return (value - from1) / (to1 - from1) * (to2 - from2) + from2

        puzzle = copy.deepcopy(solution)
        diff = scaled_clamp(
            float(difficulty_percent+1), 1.0, 100.0, 3/10, 8/10)
        base = 3
        side = base * base
        num_squares = side * side
        num_empties = int(num_squares * diff)  # number of empty values

        for subset in random.sample(range(num_squares), num_empties):
            puzzle[subset // side][subset % side] = 0
        return puzzle

    def _solve_sudoku(self, board):
        size = len(board)
        block = int(size ** 0.5)
        # Reduce array to one dimension
        board = [n for row in board for n in row]
        span = {
            (n, p): {
                (g, n) for g in
                (n > 0) * [
                    p // size,
                    size + p % size,
                    2 * size + p % size // block + p // size // block * block
                ]
            } for p in range(size * size) for n in range(size + 1)
        }
        empties = [i for i, n in enumerate(board) if n == 0]
        used = set().union(*(span[n, p] for p, n in enumerate(board) if n))
        empty = 0
        while empty >= 0 and empty < len(empties):
            pos = empties[empty]
            used -= span[board[pos], pos]
            board[pos] = next(
                (n for n in range(board[pos] + 1, size + 1)
                    if not span[n, pos] & used), 0
            )
            used |= span[board[pos], pos]
            empty += 1 if board[pos] else -1
            if empty == len(empties):
                solution = [
                    board[r:r+size] for r in range(0, size * size, size)
                ]
                yield solution
                empty -= 1
        return solution
