from brownie import Lottery, network, accounts, config


# 50/3200 ~== 0.0156
# 0.0156 * 10**18


def test_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    entranceFee = lottery.getEntranceFee()

    assert entranceFee <= (0.0166 * 10**18)
    assert entranceFee >= (0.0146 * 10**18)
