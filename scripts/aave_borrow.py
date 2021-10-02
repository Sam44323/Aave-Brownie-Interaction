from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import config, network, interface


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in [LOCAL_BLOCKCHAIN_ENVIRONMENTS, "kovan"]:
        get_weth()
    lending_pool = get_lending_pool()


# this function uses the lending pool address contract for getting the current address for the lending pool contract
# and returns it


def get_lending_pool():
    # getting the contract for the lending pool provider contract
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active(
        )]["lending_pool_addresses_provider"]
    )

    # getting the current address for the lending pool contract for aave
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
