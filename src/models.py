from pydantic import BaseModel
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


class StakePool(BaseModel):
    pid_: int
    token_name: str
    token_id: str
    pool_name: str
    my_wallet: str
    mainnet: str
    contract_: str
    contract_abi: str

    def _check(self) -> Tuple[Decimal, Decimal]:
        web3: Web3 = Web3(Web3.HTTPProvider(self.mainnet))
        wallet: ChecksumAddress = web3.toChecksumAddress(self.my_wallet)
        ct: Contract = web3.eth.contract(self.contract_, abi=self.contract_abi)
        # Call contract functions to get pool info
        staked: int = ct.functions.userInfo(self.pid_, wallet).call()[0]
        if self.token_name in ["CAKE", "WINGS"]:
            pending: int = ct.functions.pendingCake(self.pid_, wallet).call()
        else:
            pending: int = ct.functions.pending(self.pid_, wallet).call()
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
        rows: List[AssetValue] = [
            AssetValue(self.token_name, 1, staked, pending)
        ]
        for pair in pairs.split(","):
            rows.append(
                AssetValue(pair, price[pair], staked, pending)
            )
        # Create table
        table: Table = Table(title=self.pool_name, box=box.SIMPLE)
        header: List[str] = ["Value", self.token_name, "Staked", "Pending"]
        for item in header:
            table.add_column(item)
        for row in rows:
            table.add_row(row.token, row.price, row.staked, row.pending)
        # Print table
        console: Console = Console()
        console.print(table)


class AssetValue:
    def __init__(self, token: str,
                 price: float, staked: Decimal, pending: Decimal):
        self.token: str = token.upper()
        self.price: str = str(round(price, 4))
        self.staked: str = str(round(float(staked) * price, 6))
        self.pending: str = str(round(float(pending) * price, 6))


if __name__ == "__main__":
    print("This is not main!")

