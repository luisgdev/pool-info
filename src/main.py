import time

from web3 import Web3
from rich import box
from rich import console
from rich.table import Table
from rich.console import Console

import crypto_v1 as crypto
import contracts


def calc_apr(min, token):
    wallet = contracts.data[token]['my_wallet']
    init_balance = float(check_pool(wallet, token)['pending'])
    print(f'{time.strftime("%H:%M:%S")} -> {init_balance} tokens')
    time.sleep(min * 60)
    last_check = check_pool(wallet, token)
    final_balance = float(last_check['pending'])
    staked = float(last_check['staked'])
    print(f'{time.strftime("%H:%M:%S")} -> {final_balance} tokens')
    # Calc APR
    yih = (final_balance - init_balance) * (60/min)
    yihp = (yih / staked) * 100
    apr = yihp * 24 * 365
    return apr


def check_pool(wallet, token):
    bsc_mainnet = "https://bsc-dataseed3.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc_mainnet))
    #print(f'Connected to Web3: {web3.isConnected()}')
    # Pool Data
    _pid = contracts.data[token]['_pid']
    contract = contracts.data[token]['contract']
    contract_abi = contracts.data[token]['contract_abi']
    contract_info = web3.eth.contract(contract, abi=contract_abi)
    # Call contract functions to get info
    wallet = web3.toChecksumAddress(contracts.data[token]['my_wallet'])
    staked = contract_info.functions.userInfo(_pid, wallet).call()[0]
    if token.lower() == 'cake':
        pending = contract_info.functions.pendingCake(_pid, wallet).call()
    else:
        pending = contract_info.functions.pending(_pid, wallet).call()

    result = {
        'staked': web3.fromWei(staked, 'ether'),
        'pending': web3.fromWei(pending, 'ether')
    }
    return result


def view_stake(token):
    balances = check_pool(contracts.data[token]['my_wallet'], token)
    staked_balance = balances['staked']
    pending_balance = balances['pending']
    # Get current prices to calc value
    price = crypto.get_price(contracts.data[token]['token_id'], 'usd,bnb')
    token_usd = price['usd']
    staked_usd = float(staked_balance) * token_usd
    pending_usd = float(pending_balance) * token_usd
    token_bnb = price['bnb']
    staked_bnb = float(staked_balance) * token_bnb
    pending_bnb = float(pending_balance) * token_bnb
    # Create table ...
    table = Table(title=f'{contracts.data[token]["pool_name"]}', box=box.SIMPLE)
    header = ['Balance', token.upper(), 'USD Value', 'BNB Value']
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
        str(round(token_usd, 6)), 
        str(round(token_bnb, 6)))
    console = Console()
    console.print(table)


if __name__ == '__main__':
    my_pools = ['cake', 'mdx']
    init_time = time.perf_counter()
    for item in my_pools:
        view_stake(item)
    elapsed_time = round(time.perf_counter() - init_time, 2)
    print(f' *** Elapsed Time: {elapsed_time} s ***\n')
    console = Console()
    with console.status('it will take a minute') as status:
        print('Calculating APR...')
        for item in my_pools:
            apr = calc_apr(min=1, token=item)
            Console().print(f'\n {item.upper()} APR = {round(apr, 2)}%', style="bold green")
        
