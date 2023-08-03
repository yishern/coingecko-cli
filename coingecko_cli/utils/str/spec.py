import typing

from typing_extensions import TypedDict


class Grid(TypedDict):
    n_rows: int
    n_columns: int
    xmin: typing.Union[int, float]
    xmax: typing.Union[int, float]
    ymin: typing.Union[int, float]
    ymax: typing.Union[int, float]

Raster = typing.Any

GridCharDict = typing.Dict[typing.Tuple[typing.Tuple[int, ...], ...], str]
SampleMode = typing.Literal[
    'whole',
    'height_split',
    'width_split',
    'quadrants',
    'sextants',
    'braille',
]

