from brownie import Lottery, network, accounts, config
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS

# 50/3200 == 0.015625 ether
# 0.015625 * 10**18 wei


def test_get_entrance_fee():

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    ## Arrange
    lottery = deploy_lottery()
    ## Act

    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.015625, "ether")
    ## Assert
    ## 15625000000000000
    assert entrance_fee == expected_entrance_fee
