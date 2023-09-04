# -*- coding: utf-8
from copy import deepcopy
from dataclasses import dataclass
from typing import List


@dataclass
class Data():
    _data = [[0]*9 for _ in range(9)]

    def __init__(self, **kwargs):
        if 'data' in kwargs:
            # TODO type, size and range check
            self._data = deepcopy(kwargs.get('data'))

    def __getter__(self) -> List[int]:
        return self._data

    def __getitem__(self, indecies) -> int:
        if isinstance(indecies, tuple):
            col, row = indecies
            if 3 < col < 0 or 3 < row < 0:
                raise IndexError
            return self._data[col][row]

    def __setitem__(self, indecies, new_value: int):
        if isinstance(indecies, tuple):
            col, row = indecies
            if 3 < col < 0 or 3 < row < 0:
                raise IndexError
            self._data[col][row] = new_value
        else:
            raise IndexError

    def __repr__(self) -> str:
        return str(deepcopy(self._data))

    def __str__(self):
        max_num_length = len(str(max(self.flatten())))
        return '\n'.join(', '.join(
            f'{self[row, col]:{max_num_length}}'
            for col in range(9))
            for row in range(9)
        )

    def copy(self) -> List[int]:
        return deepcopy(self._data)

    def flatten(self) -> List[int]:
        return [value for row in self._data for value in row]
