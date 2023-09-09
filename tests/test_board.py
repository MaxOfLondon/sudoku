# -*- coding: utf-8
import unittest
import warnings  # noqa # used for debug: warnings.warn(UserWarning(result))
from unittest import mock
from unittest.mock import MagicMock, Mock

from src.sudoku.board import Board


class TestBoard(unittest.TestCase):
    def test_handle_number_entered(self):
        Board.cells = MagicMock()
        Board.handle_number_entered(Board, 0, 9, True)
        self.assertEqual(Board.cells[0].value, 9)
        self.assertTrue(Board.cells[0].guessed)

    def test__make_border_default(self):
        # top-left
        result = Board._make_border(Board, 0)
        self.assertEqual(result, [4, 4, 1, 1])
        # bottom-left
        result = Board._make_border(Board, 8)
        self.assertEqual(result, [4, 1, 1, 4])
        # top-right
        result = Board._make_border(Board, 9*8)
        self.assertEqual(result, [1, 4, 4, 1])
        # bottom-right
        result = Board._make_border(Board, 9*9 - 1)
        self.assertEqual(result, [1, 1, 4, 4])

        exp_results_col1 = [
            [1, 4, 1, 1], [1, 1, 1, 1], [1, 1, 1, 2],
            [1, 2, 1, 1], [1, 1, 1, 1], [1, 1, 1, 2],
            [1, 2, 1, 1], [1, 1, 1, 1], [1, 1, 1, 4]
        ]
        exp_results_col2 = [
            [1, 4, 2, 1], [1, 1, 2, 1], [1, 1, 2, 2],
            [1, 2, 2, 1], [1, 1, 2, 1], [1, 1, 2, 2],
            [1, 2, 2, 1], [1, 1, 2, 1], [1, 1, 2, 4]
        ]

        for index, exp_result in enumerate(exp_results_col1):
            print(index)
            result = Board._make_border(Board, 9 + index)
            self.assertEqual(result, exp_result)

        for index, exp_result in enumerate(exp_results_col2):
            print(index)
            result = Board._make_border(Board, 18 + index)
            self.assertEqual(result, exp_result)

    def test__make_border(self):
        result = Board._make_border(Board, 0, 1)
        self.assertEqual(result, [4, 4, 1, 1])

    def test__make_border_thick(self):
        result = Board._make_border(Board, 0, 2)
        self.assertEqual(result, [8, 8, 2, 2])

    def test_handle_deleted(self):
        Board.cells = MagicMock()
        Board.handle_number_entered(Board, 0, 9, True)
        Board.handle_deleted(Board, 0)
        self.assertEqual(Board.cells[0].value, 0)
        self.assertFalse(Board.cells[0].guessed)

    def test_set_hints(self):
        pass

    @mock.patch.object(Board, '__init__', return_value=None)
    def test_get_value(self, _):
        mock_cells = MagicMock()
        mock_cells.__len__ = Mock(return_value=1)
        mock_cells.__getitem__.return_value = Mock()
        mock_cells.__getitem__.return_value.value = 9

        board = Board()
        board.cells = mock_cells
        value = board.get_value(0)
        self.assertEqual(value, 9)

    @mock.patch.object(Board, '__init__', return_value=None)
    def test_get_value_none(self, _):
        mock_cells = MagicMock()

        board = Board()
        board.cells = mock_cells
        value = board.get_value(0)
        self.assertEqual(value, None)

    @mock.patch.object(Board, '__init__', return_value=None)
    def test__make_rect(self, _):
        def rect(*args):
            return {*args}

        with mock.patch('src.sudoku.board.pygame') as mock_pygame:
            mock_pygame.Rect = MagicMock()
            mock_pygame.Rect.side_effect = rect
            board = Board()
            board.square_size = 54
            expected = [
                {(54, 54), (0, 0)}, {(54, 54), (0, 54)},
                {(0, 108), (54, 54)}, {(54, 54), (0, 162)},
                {(0, 216), (54, 54)}, {(54, 54), (0, 270)},
                {(54, 54), (0, 324)}, {(0, 378), (54, 54)},
                {(54, 54), (0, 432)}, {(54, 54), (54, 0)}
            ]

            results = [board._make_rect(i) for i in range(10)]
            [self.assertIn(results[i], expected)
                for i, _ in enumerate(results)]

class TestBoardWithSetUp(unittest.TestCase):
    class Cell:
        def handle_clicked(self) -> None:  # pragma: no cover
            pass

        def flatten(self):  # pragma: no cover
            pass

    def setUp(self):
        with mock.patch(
            'src.sudoku.board.pygame',
            new=MagicMock()
        ) as mock_pygame:
            with mock.patch(
                'src.sudoku.board.Board.cells',
                new=MagicMock(self.Cell())
            ) as mock_cells:
                self.board = Board(
                    mock_pygame,
                    mock_cells
                )
                # self.mock_cells = mock_cells

    def test_handle_clicked(self):
        self.board.handle_clicked((10, 10))
        [cell.handle_clicked.assert_called() for cell in self.board.cells]

    def test_draw(self):
        self.board.draw()
        [cell.draw.assert_called() for cell in self.board.cells]

    def test_get_values(self):
        self.board.get_values()
        [cell.get_value.assert_called() for cell in self.board.cells]


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
