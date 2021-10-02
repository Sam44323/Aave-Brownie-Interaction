from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import config, network


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in [LOCAL_BLOCKCHAIN_ENVIRONMENTS, "kovan"]:
        get_weth()
