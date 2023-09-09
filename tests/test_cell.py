# -*- coding: utf-8
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from src.sudoku.cell import Cell


class TestCell(unittest.TestCase):

    @patch.object(Cell, '__init__', return_value=None)
    def test_draw(self, _):
        with unittest.mock.patch('src.sudoku.cell.pygame'):
            cell = Cell()
            cell._draw_background = MagicMock()
            cell._draw_border = MagicMock()
            cell._draw_number = MagicMock()
            cell._draw_selected = MagicMock()
            cell.surf = MagicMock()
            cell.parent_surf = MagicMock()
            cell.rect = MagicMock()

            cell.draw()
            cell._draw_background.assert_called_with()
            cell._draw_border.assert_called_with()
            cell._draw_number.assert_called_with()
            cell._draw_selected.assert_called_with()
            cell.parent_surf.blit.assert_called()

    @patch.object(Cell, '__init__', return_value=None)
    def test_handle_clicked(self, _):
        with unittest.mock.patch('src.sudoku.cell.pygame') as mock_pygame:
            mock_pygame.event = MagicMock()
            mock_pygame.event.post = MagicMock(side_effect=lambda *args: True)
            cell = Cell()
            cell._definite = False
            cell.rect = MagicMock()
            cell.rect.collidepoint = MagicMock(side_effect=lambda a: True)

            cell.handle_clicked((10, 10))
            mock_pygame.event.post.assert_called()

    @patch.object(Cell, '__init__', return_value=None)
    def test_toggle_hint(self, _):
        cell = Cell()
        cell._hint_on = False
        cell.toggle_hint()
        self.assertTrue(cell._hint_on)
        cell.toggle_hint()
        self.assertFalse(cell._hint_on)

    @patch.object(Cell, '__init__', return_value=None)
    def test_hint_property(self, _):
        cell = Cell()
        self.assertFalse(cell.hint)

    @patch.object(Cell, '__init__', return_value=None)
    def test_hint_setter(self, _):
        cell = Cell()
        cell.hint = True
        self.assertTrue(cell._hint_on)

    @patch.object(Cell, '__init__', return_value=None)
    def test_guessed_property(self, _):
        cell = Cell()
        self.assertFalse(cell.guessed)

    @patch.object(Cell, '__init__', return_value=None)
    def test_guessed_setter(self, _):
        cell = Cell()
        cell.guessed = True
        self.assertTrue(cell._guessed)

    @patch.object(Cell, '__init__', return_value=None)
    def test_display_property(self, _):
        cell = Cell()
        self.assertTrue(cell.display)

    @patch.object(Cell, '__init__', return_value=None)
    def test_display_setter(self, _):
        cell = Cell()
        cell.display = False
        self.assertFalse(cell._show_value)

    @patch.object(Cell, '__init__', return_value=None)
    def test_selected_property(self, _):
        cell = Cell()
        self.assertFalse(cell.selected)

    @patch.object(Cell, '__init__', return_value=None)
    def test_selected_setter(self, _):
        cell = Cell()
        cell.selected = True
        self.assertTrue(cell._selected)

    @patch.object(Cell, '__init__', return_value=None)
    def test__set_border_offset(self, _):
        cell = Cell()
        cell.border_left = cell.border_top = 1
        cell.border_right = cell.border_bottom = 1
        cell._set_border_offset()
        self.assertEqual(
            cell.border_offset,
            SimpleNamespace(left=0, top=0, right=1, bottom=1)
        )

    @patch.object(Cell, '__init__', return_value=None)
    def test__set_selected_offset(self, _):
        cell = Cell()
        self.selected_line_width = 3
        cell._set_selected_offset()
        self.assertEqual(
            cell.selected_offset,
            SimpleNamespace(left=1, top=1, right=2, bottom=2)
        )

    @patch.object(Cell, '__init__', return_value=None)
    def test__draw_background(self, _):
        cell = Cell()
        cell._set_bg_color = MagicMock()
        cell.surf = MagicMock()
        cell._draw_background()
        cell._set_bg_color.assert_called_with()
        cell.surf.fill.assert_called_with('#ffffff')

    @patch.object(Cell, '__init__', return_value=None)
    def test__set_bg_color_default(self, _):
        """Tests setting cell bg color with conditions:
        _definite = False
        _hint_on = False
        _guessed = False
        value = x
        """
        cell = Cell()
        cell._set_bg_color()
        self.assertEqual(cell.color, '#ffffff')

    @patch.object(Cell, '__init__', return_value=None)
    def test__set_bg_color_definite_is_true(self, _):
        """Tests setting cell bg color with conditions:
        _definite = True
        _hint_on = False
        _guessed = False
        value = x
        """
        cell = Cell()
        cell._definite = True
        cell._set_bg_color()
        self.assertEqual(cell.color, '#ffffcc')

    @patch.object(Cell, '__init__', return_value=None)
    def test__set_bg_color_definite_is_false_hint_on_is_true_value_0(self, _):
        """Tests setting cell bg color with conditions:
        _definite = False
        _hint_on = True
        _guessed = False
        value = 0
        """
        cell = Cell()
        cell._hint_on = True
        cell.value = 0
        cell._set_bg_color()
        self.assertEqual(cell.color, '#ffffff')

    @patch.object(Cell, '__init__', return_value=None)
    def test__set_bg_color_definite_is_false_hint_on_is_true_value_1(self, _):
        """Tests setting cell bg color with conditions:
        _definite = False
        _hint_on = True
        _guessed = False
        value = 1
        """
        cell = Cell()
        cell._hint_on = True
        cell.value = 1
        cell._set_bg_color()
        self.assertEqual(cell.color, '#ffcccc')

    @patch.object(Cell, '__init__', return_value=None)
    def test__set_bg_color_definite_is_false_hint_on_is_true_guessed_is_true(
            self, _
    ):
        """Tests setting cell bg color with conditions:
        _definite = False
        _hint_on = True
        _guessed = True
        value = x
        """
        cell = Cell()
        cell._hint_on = True
        cell._guessed = True
        cell.value = 1
        cell._set_bg_color()
        self.assertEqual(cell.color, '#ffffff')

    @patch.object(Cell, '__init__', return_value=None)
    def test__draw_number_happy(self, _):
        """
        _show_value = True
        value = 1
        """
        cell = Cell()
        cell._show_value = True
        cell.value = 1
        cell.font = MagicMock()
        cell.surf = MagicMock()
        cell._dimension = 54

        cell._draw_number()
        cell.surf.blit.assert_called()

    @patch.object(Cell, '__init__', return_value=None)
    def test__draw_number_show_value_is_false_no_blit(self, _):
        """
        _show_value = False
        value = x
        """
        cell = Cell()
        cell._show_value = False
        cell.font = MagicMock()
        cell.surf = MagicMock()
        cell._dimension = 54

        cell._draw_number()
        assert not cell.surf.blit.called

    @patch.object(Cell, '__init__', return_value=None)
    def test__draw_number_value_is_0_no_blit(self, _):
        """
        _show_value = True
        value = 0
        """
        cell = Cell()
        cell._show_value = True
        cell.value = 0
        cell.font = MagicMock()
        cell.surf = MagicMock()
        cell._dimension = 54

        cell._draw_number()
        assert not cell.surf.blit.called

    @patch.object(Cell, '__init__', return_value=None)
    def test__draw_border(self, _):
        with unittest.mock.patch('src.sudoku.cell.pygame') as mock_pygame:
            cell = Cell()
            cell.surf = MagicMock()
            cell.border_offset = MagicMock()
            cell._dimension = 54
            cell._draw_border()
            self.assertEqual(mock_pygame.draw.line.call_count, 4)

    @patch.object(Cell, '__init__', return_value=None)
    def test__draw_selected(self, _):
        with unittest.mock.patch('src.sudoku.cell.pygame') as mock_pygame:
            cell = Cell()
            cell._selected = True
            cell.surf = MagicMock()
            cell.selected_offset = MagicMock()
            cell._dimension = 54
            cell._draw_selected()
            self.assertEqual(mock_pygame.draw.line.call_count, 4)

    @patch.object(Cell, '__init__', return_value=None)
    def test__draw_selected_selected_is_false(self, _):
        with unittest.mock.patch('src.sudoku.cell.pygame') as mock_pygame:
            cell = Cell()
            cell._selected = False
            cell._draw_selected()
            self.assertEqual(mock_pygame.draw.line.call_count, 0)

    @patch('src.sudoku.cell.pygame')
    def test__init__(self, mock_pygame):
        with patch('builtins.max', return_value=54):
            rect_mock = MagicMock()
            rect_mock.rect.width.__gt__ = lambda self, compare: True

            mock_pygame.Surface.convert = MagicMock()

            cell = Cell(
                rect_mock,
                cid=100,
                is_definite=True,
                parent_surf=mock_pygame,
                border=[1, 1, 1, 1]
            )
            print(cell)
            self.assertEqual(cell.cid, 100)


if __name__ == '__main__':
    unittest.main()  # pragma no cover
