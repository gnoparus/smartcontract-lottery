from brownie import Lottery, network, accounts, config
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3

# 50/3200 ~== 0.0156
# 0.0156 * 10**18


def test_get_entrance_fee():
    ## Arrange
    lottery = deploy_lottery()
    ## Act

    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.015625, "ether")
    ## Assert
    ## 000156250000000000
    assert entrance_fee == expected_entrance_fee


# 156250000000000
# 15625000000000000
