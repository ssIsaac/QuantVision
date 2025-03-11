"""Console script for stock_prediction."""
import stock_prediction

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for stock_prediction."""
    console.print("Replace this message by putting your code into "
               "stock_prediction.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
