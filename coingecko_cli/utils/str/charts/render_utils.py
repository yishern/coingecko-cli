import typing

import numpy as np

from .. import spec
from . import char_dicts


def array_to_tuple(
    array: typing.Sequence[typing.Any],
) -> typing.Tuple[typing.Tuple[typing.Any, ...], ...]:
    return tuple(tuple(row) for row in array)

def render_supergrid(
    array,  # type: ignore
    rows_per_cell: int | None = None,
    columns_per_cell: int | None = None,
    char_dict: spec.GridCharDict | spec.SampleMode | None = None,
    color_grid = None,  # type: ignore
    color_map: typing.Mapping[int, str] | None = None,
) -> str:

    # determine chart dict and related parameters
    if char_dict is None:
        char_dict = 'whole'
    if isinstance(char_dict, str):
        char_dict = char_dicts.get_char_dict(char_dict)
    if rows_per_cell is None or columns_per_cell is None:
        single_char_index = next(iter(char_dict.keys()))
        rows_per_cell = len(single_char_index)
        columns_per_cell = len(single_char_index[0])

    array = array[::-1]
    rows, columns = array.shape
    super_rows = rows / rows_per_cell
    super_columns = columns / columns_per_cell

    new_rows = []
    super_rows = np.vsplit(array, super_rows)  # type: ignore
    for sr, super_row in enumerate(super_rows):  # type: ignore
        new_row = []
        super_cells = np.hsplit(super_row, super_columns)  # type: ignore
        for sc, super_cell in enumerate(super_cells):

            # get char
            as_tuple = array_to_tuple(super_cell)
            char_str = char_dict[as_tuple]

            # get color
            if color_grid is not None and char_str not in [' ', '⠀']:
                color = color_map[color_grid[sr, sc]]  # type: ignore
                char_str = '[' + color + ']' + char_str + '[/' + color + ']'

            new_row.append(char_str)

        new_rows.append(''.join(new_row))
    return '\n'.join(new_rows)
