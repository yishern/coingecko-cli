import typing

from typing_extensions import Literal

from .. import spec
from . import grid_utils, line_utils


def create_blank_raster(
    grid: spec.Grid,
    container_format: Literal[
        'array', 'list_of_rows', 'list_of_columns'
    ] = 'array',
    cell_format: typing.Type[int] | typing.Type[str] = int,
) -> str:
    if container_format == 'array':
        import numpy as np

        if cell_format == int:
            return np.zeros((grid['n_rows'], grid['n_columns']), dtype=int)
        elif cell_format is str:
            return np.zeros((grid['n_rows'], grid['n_columns']), dtype='<U1')
        else:
            raise Exception('unknown cell format: ' + str(cell_format))

    elif container_format == 'list_of_rows':
        if cell_format is int:
            cell: int | float | str = 0
        elif cell_format is str:
            cell = ' '
        else:
            raise Exception('unknown cell format: ' + str(cell_format))

        return [[[cell] * grid['n_columns']] for row in range(grid['n_rows'])]

    elif container_format == 'list_of_columns':
        if cell_format is int:
            cell = 0
        elif cell_format is str:
            cell = ' '
        else:
            raise Exception('unknown cell format: ' + str(cell_format))

        return [[[cell] * grid['n_rows']] for row in range(grid['n_columns'])]

    else:
        raise Exception('unknown container_format: ' + str(container_format))


def rasterize_by_lines(
    yvals: typing.Sequence[int | float],
    grid: spec.Grid,
) -> spec.Raster:

    # trunk-ignore(bandit/B101)
    assert len(yvals) == grid['n_columns']

    raster = create_blank_raster(grid)
    for column, yval in enumerate(yvals[:-1]):
        row = grid_utils.get_row(yval, grid)
        row_next = grid_utils.get_row(yvals[column + 1], grid)

        rows, columns = line_utils.draw_line(
            row,
            column,
            row_next,
            column + 1,
        )
        mask = (rows >= 0) * (columns >= 0)  # type: ignore
        raster[rows[mask], columns[mask]] = 1

    return raster
