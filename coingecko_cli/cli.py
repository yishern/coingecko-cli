import typer

app = typer.Typer(rich_markup_mode="rich")

@app.command()
def test():
    pass