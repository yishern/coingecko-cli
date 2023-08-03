import typing

import numpy as np

from .. import spec


def get_row_borders(grid: spec.Grid):
    return np.linspace(grid['ymin'], grid['ymax'], grid['n_rows'] + 1)


def get_row(
    yval: typing.Union[typing.SupportsInt, typing.SupportsFloat],
    grid: spec.Grid,
) -> int:
    row_borders = get_row_borders(grid)
    if yval < row_borders[0]:
        return -1
    elif yval > row_borders[-1]:
        return grid['n_rows']
    else:
        import numpy as np

        return np.searchsorted(row_borders, yval) - 1  # type: ignore

def get_rows(
    yvals: typing.Sequence[typing.SupportsInt | typing.SupportsFloat],
    grid: spec.Grid,
) -> typing.Sequence[int]:

    import numpy as np

    row_borders = get_row_borders(grid)
    plural_results: typing.Sequence[int] = np.searchsorted(row_borders, yvals) - 1  # type: ignore
    return plural_results
