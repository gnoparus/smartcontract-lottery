from brownie import Lottery, network, accounts, config, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
)

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


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    ## Arrange
    lottery = deploy_lottery()

    ## Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee() + 100})


def test_can_start_and_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    ## Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})

    ## Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 100})

    ## Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    ## Arrange
    lottery = deploy_lottery()
    account = get_account()

    ## Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 100})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})

    ## Assert
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    ## Arrange
    lottery = deploy_lottery()
    account = get_account()

    ## Act
    lottery.startLottery({"from": account})

    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 100})

    lottery.enter(
        {"from": get_account(index=1), "value": lottery.getEntranceFee() + 200}
    )
    lottery.enter(
        {"from": get_account(index=2), "value": lottery.getEntranceFee() + 300}
    )

    #### 779 MOD 3 == 2
    STATIC_RNG = 779
    EXPECTED_WINNER_IDX = 2

    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    prev_balance = get_account(index=EXPECTED_WINNER_IDX).balance()
    lottery_balance = lottery.balance()
    request_id = transaction.events["RequestedRandomness"]["requestId"]

    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )

    ## Assert
    assert lottery.recentWinner() == get_account(index=EXPECTED_WINNER_IDX)
    assert lottery.balance() == 0
    assert get_account(index=EXPECTED_WINNER_IDX).balance() == (
        prev_balance + lottery_balance
    )
