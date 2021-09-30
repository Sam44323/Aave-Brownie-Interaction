from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def get_weth():
    account = get_account()
    weth = interface.IWeth(
        config["networks"][network.show_active()]["weth_token"])


def main():
    get_weth()
