import web3
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import config, network, interface
from web3 import Web3

# 0.1
AMOUNT = Web3.toWei(0.1, 'ether')


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in [LOCAL_BLOCKCHAIN_ENVIRONMENTS, "kovan"]:
        get_weth()
    lending_pool = get_lending_pool()
    # allowing the contract to spend the erc20 tokens
    approve_erc20(AMOUNT, erc20_address, lending_pool.address, get_account())
    print("Depositing!")
    transaction = lending_pool.deposit(erc20_address, Web3.toWei(
        0.000001, 'ether'), account.address, 0, {"from": account})
    transaction.wait(1)
    print("Deposited!")
    (borrowable_eth, total_debt) = get_borrowable_data(lending_pool, account)
    print("Borrowing assets!")
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]['dai_eth_price_feed'])
    amount_dai_to_borrow = (1/dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    dai_token_address = config["networks"][network.show_active()]["dai_token"]
    transaction = lending_pool.borrow(
        dai_token_address, Web3.toWei(amount_dai_to_borrow, "ether"), 1, 0, account.address)
    transaction.wait(1)

# this function uses the lending pool provider address contract for getting the current address for the lending pool contract and returns it


def get_lending_pool():
    # getting the contract for the lending pool provider contract
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active(
        )]["lending_pool_address_provider"]
    )

    # getting the current address for the lending pool contract for aave
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

# Function for approving the ERC20 token for any transaction


def approve_erc20(amount, erc20_address, spender, account):
    print("Approving the ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    transaction = erc20.approve(spender, amount,  {"from": account})
    transaction.wait(1)
    print("Approved!")
    return transaction


def get_borrowable_data(lending_pool, account):
    (total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_threshold,
     ltv, h_factor) = lending_pool.getUserAccountData(account.address)
    # converting the returned wei data to ether
    available_borrow_eth = Web3.fromWei(available_borrow_eth, 'ether')
    total_collateral_eth = Web3.fromWei(total_collateral_eth, 'ether')
    total_debt_eth = Web3.fromWei(total_debt_eth, 'ether')
    return(float(available_borrow_eth), float(total_debt_eth))

# for getting the asset price from chainlink


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3(price_feed_address)
    # getting the latest round price
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    # converting the value from wei to ether
    latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {latest_price}")
    return float(latest_price)
