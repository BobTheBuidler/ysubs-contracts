
import brownie

from fixtures import MAX_POOL_CT, _from, lusd_contract, subscriber_contract


def test_subscribe(subscriber_contract, lusd_contract, accounts):
    owner, user = accounts[0], accounts[1]
    minter = lusd_contract.borrowerOperationsAddress()
    for i in range(1, MAX_POOL_CT):
        amount = i*10**18
        with brownie.reverts('Plan does not exist or has been retired.'):
            subscriber_contract.subscribe(i, amount, _from(user))
        subscriber_contract.create_plan(amount/10**10, _from(owner))
        subscriber_contract.activate_plan(i, _from(owner))
        with brownie.reverts('ERC20: transfer amount exceeds balance'):
            subscriber_contract.subscribe(i, amount, _from(user))
        lusd_contract.mint(user, amount, _from(minter))
        with brownie.reverts('ERC20: transfer amount exceeds allowance'):
            subscriber_contract.subscribe(i, amount, _from(user))
        lusd_contract.approve(subscriber_contract, amount, _from(user))
        subscriber_contract.subscribe(i, amount, _from(user))
        assert subscriber_contract.subscription_end(i, user) > 0
        

def test_subscribe_for(subscriber_contract, lusd_contract, accounts):
    owner, user, helper = accounts[0], accounts[1], accounts[3]
    minter = lusd_contract.borrowerOperationsAddress()
    for i in range(1, MAX_POOL_CT):
        amount = i*10**18
        with brownie.reverts('Plan does not exist or has been retired.'):
            subscriber_contract.subscribe_for(i, amount, user, _from(helper))
        subscriber_contract.create_plan(amount/10**10, _from(owner))
        subscriber_contract.activate_plan(i, _from(owner))
        with brownie.reverts('ERC20: transfer amount exceeds balance'):
            subscriber_contract.subscribe_for(i, amount, user, _from(helper))
        lusd_contract.mint(user, amount, _from(minter))
        with brownie.reverts('ERC20: transfer amount exceeds allowance'):
            subscriber_contract.subscribe_for(i, amount, user, _from(helper))
        lusd_contract.approve(subscriber_contract, amount, _from(user))
        subscriber_contract.subscribe_for(i, amount, user, _from(helper))
        assert subscriber_contract.subscription_end(i, user) > 0