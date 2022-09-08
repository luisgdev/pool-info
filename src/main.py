from typing import List, Optional
from rich.console import Console
import typer

from models import StakePool
import pools


WAIT_MESSAGE: str = "it will take a minute"

app = typer.Typer()


@app.command()
def main(symbol: str, apr: Optional[str] = None):
    my_pools: List[str] = symbol.split(",")
    for pool in my_pools:
        my_stake: StakePool = StakePool(**pools.data[pool])
        my_stake.print_view(pairs="usd,bnb")
        console: Console = Console()
        if apr:
            with console.status(WAIT_MESSAGE) as status:
                print("Calculating APR...")
                apr: float = my_stake.calc_apr()
                Console().print(
                    f"APR = {round(apr, 2)}%", style="bold green"
                )


if __name__ == "__main__":
    app()

