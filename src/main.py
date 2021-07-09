import time

from web3 import Web3
from rich import box
from rich import console
from rich.table import Table
from rich.console import Console

import crypto_v1 as crypto
import pancakeswap
import res


def calc_apr(min):
    init_balance = float(check_pool(res.wallet2)['pending'])
    print(f'{time.strftime("%H:%M:%S")} -> {init_balance} tokens')
    time.sleep(min * 60)
    last_check = check_pool(res.wallet2)
    final_balance = float(last_check['pending'])
    staked = float(last_check['staked'])
    print(f'{time.strftime("%H:%M:%S")} -> {final_balance} tokens')
    # Calc APR
    yih = (final_balance - init_balance) * (60/min)
    yihp = (yih / staked) * 100
    apr = yihp * 24 * 365
    return apr


def check_pool(wallet):
    bsc_mainnet = "https://bsc-dataseed3.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc_mainnet))
    #print(f'Connected to Web3: {web3.isConnected()}')
    # PancakeSwap: Main Staking Contract (Manual Pool)
    contract = pancakeswap.manual_pool_contract
    contract_abi = pancakeswap.manual_pool_contract_abi
    contract_info = web3.eth.contract(contract, abi=contract_abi)
    # Call contract functions to get data
    wallet = web3.toChecksumAddress(wallet)
    staked = contract_info.functions.userInfo(0, wallet).call()[0]
    pending = contract_info.functions.pendingCake(0, wallet).call()
    result = {
        'staked': web3.fromWei(staked, 'ether'),
        'pending': web3.fromWei(pending, 'ether')
    }
    return result


def view_stake():
    balances = check_pool(res.wallet2)
    staked_balance = balances['staked']
    pending_balance = balances['pending']
    # Get current prices to calc value
    price = crypto.get_price('pancakeswap-token', 'usd,bnb')
    cake_usd = price['usd']
    staked_usd = float(staked_balance) * cake_usd
    pending_usd = float(pending_balance) * cake_usd
    cake_bnb = price['bnb']
    staked_bnb = float(staked_balance) * cake_bnb
    pending_bnb = float(pending_balance) * cake_bnb
    # Create table ...
    table = Table(title='\U0001F95E PancakeSwap Main Pool', box=box.SIMPLE)
    header = ['Balance', 'CAKE', 'USD Value', 'BNB Value']
    for item in header:
        table.add_column(item)
    table.add_row(
        'Staked', 
        str(round(staked_balance, 4)), 
        str(round(staked_usd, 4)), 
        str(round(staked_bnb, 6)))
    table.add_row(
        'Pending', 
        str(round(pending_balance, 6)), 
        str(round(pending_usd, 6)), 
        str(round(pending_bnb, 6)))
    table.add_row(
        'Price', 
        str('1'), 
        str(round(cake_usd, 6)), 
        str(round(cake_bnb, 6)))
    console = Console()
    console.print(table)


if __name__ == '__main__':
    init_time = time.perf_counter()
    view_stake()
    elapsed_time = round(time.perf_counter() - init_time, 2)
    print(f' *** Elapsed Time: {elapsed_time} s ***\n')
    console = Console()
    print('Calculating APR...')
    with console.status('it will take a minute') as status:
        apr = calc_apr(min=1)
        Console().print(f'\nAPR = {round(apr, 2)}%', style="bold green")
