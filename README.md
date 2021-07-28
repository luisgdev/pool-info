# pool-info

This console application can show your staked and pending balances you have in a staking pool like PancakeSwap (Binance Smart Chain).

I made it to query Manual Cake pool, where staked and reward token are the same which allows you to do [compound interest](https://github.com/luisgdev/farm-calc). 
You can query other pools by modifying `pid`, `contract` and `contract_abi`.
Now you can add `mainnet` to get data from any Ethereum based blockchain.

Tested on:
- [PancakeSwap Manual Cake pool](https://bscscan.com/address/0x73feaa1eE314F8c655E354234017bE2193C9E24E#code)
- [MDEX Boardroom MDX pool](https://bscscan.com/address/0x6aEE12e5Eb987B3bE1BA8e621BE7C4804925bA68#code)

To do:
- Test with other Ethereum based blockchains like Polygon.
- Add support for pools which different rewards token.

The GUI looks nice thanks to [Rich](https://github.com/willmcgugan/rich). 

![Web3](https://img.shields.io/badge/-Web3.py-gray?style=flat&logo=ethereum)
![BSC](https://img.shields.io/badge/-BSC-gray?style=flat&logo=binance)
![PancakeSwap](https://img.shields.io/badge/-%F0%9F%A5%9E%20PancakeSwap-gray?style=flat)
