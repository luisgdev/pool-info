from typing import List
from rich.console import Console
import typer

from models import StakePool
import pools

app = typer.Typer()
@app.command()
def main(symbol: str):
    my_pools: List[str] = symbol.split(",")
    for pool in my_pools:
        my_stake: StakePool = StakePool(**pools.data[pool])
        my_stake.print_view(pairs="usd,bnb")
        console: Console = Console()
        with console.status("it will take a minute") as status:
            print("Calculating APR...")
            apr: float = my_stake.calc_apr()
            Console().print(f"\nAPR = {round(apr, 2)}%", style="bold green")


if __name__ == "__main__":
    app()

