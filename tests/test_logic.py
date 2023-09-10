# -*- coding: utf-8
import unittest

from src.sudoku.logic import Logic


class TestLogic(unittest.TestCase):
    def setUp(self):
        self.logic = Logic()
        self.solution = [
            [2, 8, 4, 3, 7, 5, 6, 1, 9],
            [9, 6, 1, 8, 4, 2, 3, 7, 5],
            [5, 3, 7, 6, 1, 9, 8, 4, 2],
            [8, 7, 2, 1, 5, 3, 4, 9, 6],
            [3, 1, 5, 4, 9, 6, 7, 2, 8],
            [6, 4, 9, 7, 2, 8, 1, 5, 3],
            [7, 5, 8, 9, 3, 1, 2, 6, 4],
            [1, 9, 3, 2, 6, 4, 5, 8, 7],
            [4, 2, 6, 5, 8, 7, 9, 3, 1]
        ]

    def test_create_solution_success(self):
        solution = self.logic._create_solution()
        self.assertEqual(len(solution), 9)
        self.assertEqual(len(solution[0]), 9)
        self.assertNotIn(0, solution)

        flat_solution = [value for row in solution for value in row]
        for value in range(1, 9):
            self.assertEqual(flat_solution.count(value), 9)

    def test_create_puzzle_success(self):
        puzzle = self.logic._create_puzzle(self.solution, 50)
        self.assertEqual(len(puzzle), 9)
        self.assertEqual(len(puzzle[0]), 9)

        flat_puzzle = [value for row in puzzle for value in row]
        self.assertEqual(flat_puzzle.count(0), 44)

    def test_create_puzzle_min_difficulty_zero_count_24(self):
        puzzle = self.logic._create_puzzle(self.solution, 0)
        flat_puzzle = [value for row in puzzle for value in row]
        self.assertEqual(flat_puzzle.count(0), 24)

    def test_create_puzzle_max_difficulty_zero_count_65(self):
        puzzle = self.logic._create_puzzle(self.solution, 100)
        flat_puzzle = [value for row in puzzle for value in row]
        self.assertEqual(flat_puzzle.count(0), 65)

    def test_create_game_success(self):
        solution, puzzle = self.logic.create_game()
        flat_solution = [value for row in solution for value in row]
        flat_puzzle = [value for row in puzzle for value in row]
        result = [s - p for s, p in zip(flat_solution, flat_puzzle)]
        self.assertEqual(result.count(0), 81 - flat_puzzle.count(0))

    def test_is_game_over_success(self):
        self.assertTrue(self.logic.is_game_over(self.solution, self.solution))

    def test_is_game_over_fail(self):
        inputs = [0]
        self.assertFalse(self.logic.is_game_over(inputs, self.solution))

    def test__solve_sudoku(self):
        puzzle = self.logic._create_puzzle(self.solution, 50)
        result = list(self.logic._solve_sudoku(puzzle))
        self.assertIn(self.solution, result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
