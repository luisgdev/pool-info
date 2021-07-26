import time

from web3 import Web3
from rich import box
from rich.table import Table
from rich.console import Console

import market
import pools


class StakePool:

    def __init__(self, data):
        self._pid = data['_pid']
        self.token_name = data['token_name']
        self.token_id = data['token_id']
        self.pool_name = data['pool_name']
        self.my_wallet = data['my_wallet']
        self.mainnet = data['mainnet']
        self.contract = data['contract']
        self.contract_abi = data['contract_abi']

    def _check(self):
        web3 = Web3(Web3.HTTPProvider(self.mainnet))
        print(f'Connected to Web3: {web3.isConnected()}')
        wallet = web3.toChecksumAddress(self.my_wallet)
        pool = web3.eth.contract(self.contract, abi=self.contract_abi)
        # Call contract functions to get pool info
        staked = pool.functions.userInfo(self._pid, wallet).call()[0]
        if self.token_name.lower() == 'cake':
            pending = pool.functions.pendingCake(self._pid, wallet).call()
        else:
            pending = pool.functions.pending(self._pid, wallet).call()
        # Convert to readable number
        staked = float(web3.fromWei(staked, 'ether'))
        pending = float(web3.fromWei(pending, 'ether'))
        return staked, pending

    def calc_apr(self, t_min=1):
        init_pending = self._check()[1]
        print(f'{time.strftime("%H:%M:%S")} -> {init_pending} tokens')
        time.sleep(t_min * 60)
        final_staked, final_pending = self._check()
        print(f'{time.strftime("%H:%M:%S")} -> {final_pending} tokens')
        # Calc yield per hour and apr%
        yield_per_h = (final_pending - init_pending) * (60 / t_min)
        apr_p = (yield_per_h / final_staked) * 24 * 365 * 100
        return apr_p

    def print_view(self, pairs='usd,bnb,btc'):
        # Get pool info
        staked_balance, pending_balance = self._check()
        # Get market price
        price = market.get_price(self.token_id, pairs)
        # Generate rows
        rows = [
            {
                'name': self.token_name,
                'price': '1',
                'staked': str(round(staked_balance, 6)),
                'pending': str(round(pending_balance, 6))
            }
        ]
        if pairs:
            for pair in pairs.split(','):
                rows.append(
                    dict(
                        name=pair.upper(),
                        price=str(round(price[pair], 6)),
                        staked=str(round(staked_balance * price[pair], 6)),
                        pending=str(round(pending_balance * price[pair], 6))
                    )
                )
        # Create table
        table = Table(title=self.pool_name, box=box.SIMPLE)
        header = ['Value', self.token_name, 'Staked', 'Pending']
        for item in header:
            table.add_column(item)
        for r in rows:
            table.add_row(r['name'], r['price'], r['staked'], r['pending'])
        # Print table
        console = Console()
        console.print(table)


if __name__ == '__main__':
    my_stake = StakePool(pools.data['cake'])
    my_stake.print_view(pairs='usd,bnb')
    console = Console()
    with console.status('it will take a minute') as status:
        print('Calculating APR...')
        apr = my_stake.calc_apr()
        Console().print(f'\nAPR = {round(apr, 2)}%', style="bold green")
