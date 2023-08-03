import webbrowser
from typing import List, Union

from pydantic import BaseModel
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

from coingecko_cli.utils.coingecko_utils import get_market_data
from coingecko_cli.utils.str.charts import braille_utils

console = Console()
labels = ['Coin', 'Price', 'Δ 1h', 'Δ 24h', 'Δ 7d', '24h Volume', 'Mkt Cap', "Last 7 Days"]
terminal_styling = {
    "symbol": lambda x: x.upper(),
    "price_change_percentage_1h_in_currency": lambda x: Text(f"${round(x, 2)} %", style=color_polarity(x)),
    "price_change_percentage_24h_in_currency": lambda x: Text(f"${round(x, 2)} %", style=color_polarity(x)),
    "price_change_percentage_7d_in_currency": lambda x: Text(f"${round(x, 2)} %", style=color_polarity(x)),
    "total_volume": lambda x: f"${to_billions_or_millions(x)}",
    "market_cap": lambda x: f"${to_billions_or_millions(x)}",
    "sparkline": lambda x: Text(x['sparkline'], style=f"#555555 bold {color_polarity(x['price'][-1] - x['price'][0])}")
}
class Sparkline(BaseModel):
    price: List[float]
    sparkline: str

class MarketRowData(BaseModel):
    symbol: str
    current_price: float
    price_change_percentage_1h_in_currency: float
    price_change_percentage_24h_in_currency: float
    price_change_percentage_7d_in_currency: float
    total_volume: float
    market_cap: int
    sparkline: Sparkline
    def __init__(self, width, height, **data):
        price = data["sparkline_in_7d"]["price"]
        sparkline = braille_utils.create_braille_sparkline(
            data=price,
            width=width,
            height=height
        )
        super().__init__(sparkline=Sparkline(sparkline=sparkline, price=price), **data)

def to_billions_or_millions(x: Union[int, float]) -> str:
    if x > 1e9:
        return f'{x / 1e9:.2f}B'
    if x > 1e6:
        return f'{x / 1e6:.2f}M'
    return f'{x:.2f}'

def color_polarity(value: int | float | None) -> str:
    if value is None:
        return ''

    if value > 0:
        return "#8dc647"
    elif value < 0:
        return "#e15241"
    else:
        return "gray"

def terminal_print_market_data(data: List[MarketRowData]):
    table = Table(title="Coingecko", box=box.MINIMAL, title_style="bold cyan")
    for _label in labels:
        table.add_column(_label, justify="right")
    for i, row in enumerate(data):
        table.add_row(*([str(i + 1)] + [terminal_styling[key](item) if key in terminal_styling else str(item) for key, item in row.model_dump().items()]))
    console.print(table)

def market_command(
    web:bool = False,
    per_page: int = 100,
    page: int = 1,
) -> None:
    if web:
        webbrowser.open("https://www.coingecko.com")
    else:
        data = get_market_data(page=page, per_page=per_page)
        data: List[MarketRowData] = [MarketRowData(width=8, height=1, **row) for row in data]
        terminal_print_market_data(data)