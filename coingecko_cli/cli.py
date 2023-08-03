from typing import Optional

import typer
from typing_extensions import Annotated

from coingecko_cli.commands.market import market_command

app = typer.Typer(rich_markup_mode="rich")
COMMAND_EPILOG = "Powered by [bold green]CoinGecko[/bold green] :heart:"

@app.command(epilog=COMMAND_EPILOG)
def market(
    page: Annotated[Optional[int], typer.Option("--page", "-p", help="Page through results")] = 1,
    per_page: Annotated[Optional[int], typer.Option("--per-page", "-pp", help="Total results per page")] = 100,
    # web: bool = False,
    web: Annotated[Optional[bool], typer.Option("--web", "-w", help="Open in web browser")] = False,
):
    # trunk-ignore(ruff/D400)
    # trunk-ignore(ruff/D415)
    """Cryptocurrency prices
    """
    market_command(web=web, page=page, per_page=per_page)