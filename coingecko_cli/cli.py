from typing import Optional

import typer
from typing_extensions import Annotated

from coingecko_cli.commands.market import market_command
from coingecko_cli.commands.sync import sync_tokens_to_local_storage
from coingecko_cli.commands.token import autocomplete_token, token_command

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

@app.command(epilog=COMMAND_EPILOG)
def token(
    token: Annotated[str, typer.Option("--token", "-t", autocompletion=autocomplete_token, help="bitcoin ethereum", show_default=False)],
    days: Annotated[int, typer.Option("--days", "-d", help="Data up to number of days ago (e.g. 1,14,30,max)")] = 30,
    web: bool = False,
):
    # trunk-ignore(ruff/D400)
    # trunk-ignore(ruff/D415)
    """Token historical market data
    """
    token_command(web=web, token=token, days=days)

@app.command(epilog=COMMAND_EPILOG)
def sync():
    # trunk-ignore(ruff/D400)
    # trunk-ignore(ruff/D415)
    """Cache tokens locally for `token` command autocompletion"""
    sync_tokens_to_local_storage()