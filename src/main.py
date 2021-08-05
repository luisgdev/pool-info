from typing import Dict, List, Tuple
from decimal import Decimal
import time

from web3 import Web3
from rich import box
from rich.table import Table
from rich.console import Console
from web3.contract import Contract
from eth_typing.evm import ChecksumAddress

import market
import pools


class StakePool:
    def __init__(self, data: dict):
        self._pid: int = data["_pid"]
        self.token_name: str = data["token_name"]
        self.token_id: str = data["token_id"]
        self.pool_name: str = data["pool_name"]
        self.my_wallet: str = data["my_wallet"]
        self.mainnet: str = data["mainnet"]
        self.contract: str = data["contract"]
        self.contract_abi: str = data["contract_abi"]

    def _check(self) -> Tuple[Decimal, Decimal]:
        web3: Web3 = Web3(Web3.HTTPProvider(self.mainnet))
        wallet: ChecksumAddress = web3.toChecksumAddress(self.my_wallet)
        ct: Contract = web3.eth.contract(self.contract, abi=self.contract_abi)
        # Call contract functions to get pool info
        staked: int = ct.functions.userInfo(self._pid, wallet).call()[0]
        if self.token_name in ["CAKE", "WINGS"]:
            pending: int = ct.functions.pendingCake(self._pid, wallet).call()
        else:
            pending: int = ct.functions.pending(self._pid, wallet).call()
        # Convert to readable number
        staked_balance: Decimal = web3.fromWei(staked, "ether")
        pending_balance: Decimal = web3.fromWei(pending, "ether")
        return staked_balance, pending_balance

    def calc_apr(self, t_min: int = 1) -> float:
        init_pending: Decimal = self._check()[1]
        print(f'{time.strftime("%H:%M:%S")} -> {init_pending} tokens')
        time.sleep(t_min * 60)
        final_staked, final_pending = self._check()
        print(f'{time.strftime("%H:%M:%S")} -> {final_pending} tokens')
        # Calc yield per hour and apr%
        yield_per_h = float(final_pending - init_pending) * (60 / t_min)
        apr_p: float = (yield_per_h / float(final_staked)) * 24 * 365 * 100
        return apr_p

    def print_view(self, pairs: str = "usd,bnb,btc") -> None:
        # Get pool info
        staked, pending = self._check()
        # Get market price
        price: dict = market.get_price(self.token_id, pairs)
        # Generate rows
        rows: List[Dict[str, str]] = [
            {
                "name": self.token_name,
                "price": str(1),
                "staked": str(round(staked, 6)),
                "pending": str(round(pending, 6)),
            }
        ]
        for pair in pairs.split(","):
            rows.append(
                {
                    "name": pair.upper(),
                    "price": str(round(price[pair], 6)),
                    "staked": str(round(float(staked) * price[pair], 6)),
                    "pending": str(round(float(pending) * price[pair], 6)),
                }
            )
        # Create table
        table: Table = Table(title=self.pool_name, box=box.SIMPLE)
        header: List[str] = ["Value", self.token_name, "Staked", "Pending"]
        for item in header:
            table.add_column(item)
        for ro in rows:
            table.add_row(ro["name"], ro["price"], ro["staked"], ro["pending"])
        # Print table
        console: Console = Console()
        console.print(table)


if __name__ == "__main__":
    my_pools: List[str] = ["cake", "wings"]
    for pool in my_pools:
        my_stake: StakePool = StakePool(pools.data[pool])
        my_stake.print_view(pairs="usd,bnb")
        console: Console = Console()
        with console.status("it will take a minute") as status:
            print("Calculating APR...")
            apr: float = my_stake.calc_apr()
            Console().print(f"\nAPR = {round(apr, 2)}%", style="bold green")
