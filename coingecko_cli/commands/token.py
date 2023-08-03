import datetime
import webbrowser
from typing import List, Mapping, Union

import plotext as plt
from pydantic import BaseModel
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from coingecko_cli.commands.sync import read_tokens_to_local_storage
from coingecko_cli.utils.coingecko_utils import get_token_data

console = Console()

class MarketData(BaseModel):
    market_cap_rank: int
    price: float
    atl: float
    ath: float
    total_volume: int
    market_cap: int
    fdv: int
    circulating_supply: float
    total_supply: float
    price_changes: Mapping[str, float]

class MarketChart(BaseModel):
    title: str
    data: List[List[Union[int, float]]]

def format_chart_title(title: str) -> str:
    title = title.replace("_", " ")
    title = title.split()
    return " ".join([t.capitalize() for t in title])

class TokenData(BaseModel):
    name: str
    market_data: MarketData
    market_charts: List[MarketChart]
    def __init__(self, token_info: dict, market_data: dict, market_charts: dict):
        super().__init__(
            name=token_info["name"],
            market_data=MarketData(
                market_cap_rank=token_info["market_cap_rank"],
                price=market_data["current_price"]["usd"],
                atl=market_data["atl"]["usd"],
                ath=market_data["ath"]["usd"],
                total_volume=market_data["total_volume"]["usd"],
                market_cap=market_data["market_cap"]["usd"],
                fdv=market_data["fully_diluted_valuation"]["usd"],
                circulating_supply=market_data["circulating_supply"],
                total_supply=market_data["total_supply"],
                price_changes = {key: market_data[f"price_change_percentage_{key}"] for key in ["24h", "7d", "14d", "30d", "1y"]}
            ),
            market_charts=[MarketChart(title=format_chart_title(mk), data=market_charts[mk]) for mk in ["prices", "total_volumes", "market_caps"]]
        )

def format_number(number, prefix='', trailing_zeros=False, decimal=2):
    if isinstance(number, (int, float)):
        if trailing_zeros:
            number_format = "{:" + str(decimal) + ",." + str(decimal) + "f}"
        else:
            number_format = "{:3,}"
        formatted_number = number_format.format(number)
        return prefix + formatted_number
    else:
        return "Invalid input. Please provide a number."
def categorize_large_number(number):
    if number >= 1e9:
        return round(number / 1e9, 2), "B"
    elif number >= 1e6:
        return round(number / 1e6, 2), "M"
    elif number >= 1e3:
        return round(number / 1e3, 2), "K"
    else:
        return round(number, 2), None

def format_y_axis(ys: List[Union[int, float]]):
    ys = [categorize_large_number(n) for n in ys]
    ns, cs = zip(*ys, strict=False)
    return ns, [f"{_ns} {_cs}" for _ns, _cs in zip(ns, cs)]

terminal_styling = {
    "price": {"title": "Price", "f": lambda x: format_number(x, prefix="$", trailing_zeros=True)},
    "atl": {"title": "ATL", "f": lambda x: format_number(x, trailing_zeros=True, prefix="$")},
    "ath": {"title": "ATH", "f": lambda x: format_number(x, trailing_zeros=True, prefix="$")},
    "total_volume": {"title": "Total Volume", "f": lambda x: format_number(x, trailing_zeros=False)},
    "market_cap": {"title": "Market Cap", "f": lambda x: format_number(x, trailing_zeros=False, prefix="$")},
    "fdv": {"title": "FDV", "f": lambda x: format_number(x, prefix="$")},
    "circulating_supply": {"title": "Circulating Supply", "f": lambda x: format_number(x, trailing_zeros=True)},
    "total_supply": {"title": "Total Supply", "f": lambda x: format_number(x, trailing_zeros=True)},
    "price_changes": {"f": lambda x: Text(f"{x}%", style="dark_sea_green2" if x > 0 else "red")}
}

def terminal_print_token_data(data:TokenData):
    console.print(Panel.fit(f"[bold cyan]{data.name}[/bold cyan] (Data from [bold green]CoinGecko[/bold green])", style="bold"))
    console.print(Text("Statistics", style="underline bold"))
    table = Table(show_header=False, show_lines=False, box=box.MINIMAL)
    table.add_column(style="dark_cyan")
    table.add_column(style="pale_turquoise1")
    market_data = data.market_data
    for key, value in market_data.model_dump(exclude={"price_changes"}).items():
        stylizer = terminal_styling.get(key)
        if stylizer:
            title = stylizer.get("title")
            display_data = stylizer.get("f")(value)
        else:
            title = key
            display_data = str(value)

        table.add_row(title, display_data)
    console.print(table)

    console.print(Text("Charts", style="underline bold"))
    plt.plotsize(80, 36)
    plt.subplots(len(data.market_charts),1)
    plt.xfrequency(3)
    plt.theme("clear")
    plt.ticks_color(159)

    for i, market_chart in enumerate(data.market_charts):
        market_chart_title = market_chart.title
        market_chart_data = market_chart.data
        subplot = plt.subplot(i + 1, 1)
        plt.title(market_chart_title)
        x = [d[0] for d in market_chart_data]
        x = [datetime.datetime.fromtimestamp(_x / 1000).strftime("%d/%m/%Y") for _x in x]
        y = [d[1] for d in market_chart_data]
        y, y_label = format_y_axis(y)
        subplot.yticks(y, y_label)
        subplot.plot(x, y, marker="braille", color=157)
    plt.show()
    console.print("")

    price_change_keys = ["24h", "7d", "14d", "30d", "1y"]
    price_change_table = Table(width=80)
    for k in price_change_keys:
        price_change_table.add_column(k, justify="center", style="bold")
    price_change_row = []
    price_change_stylizer = terminal_styling.get("price_changes")["f"]
    for k in price_change_keys:
        pcp = round(data.market_data.price_changes[k], 2)
        price_change_row.append(price_change_stylizer(pcp))
    price_change_table.add_row(*price_change_row)
    console.print(price_change_table)

def token_command(
    web:bool,
    token: str,
    days: int,
) -> None:
    if web:
        webbrowser.open(f"https://www.coingecko.com/en/coins/{token}")
    else:
        data = get_token_data(token_id=token, days=days)
        token_info, market_charts = data["token_info"], data["market_chart"]
        market_data = token_info["market_data"]
        token_data = TokenData(
            token_info=token_info,
            market_charts=market_charts,
            market_data=market_data,
        )
        terminal_print_token_data(token_data)

def autocomplete_token(token_str: str):
    tokens = read_tokens_to_local_storage()["tokens"]
    completion = []
    for token in tokens:
        for v in token.values():
            if v.lower().startswith(token_str):
                completion.append((token['id'], f"{token['name']} <{token['symbol']}>"))
                continue
    return completion