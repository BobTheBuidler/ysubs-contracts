import brownie

from fixtures import _from, subscriber_contract, MAX_POOL_CT

RATE_LIMIT = 100
TIME_INTERVAL = 60 * 60 * 24  # one day

def test_create_plan(subscriber_contract, accounts):
    owner, bad_guy = accounts[0], accounts[1]
    for i in range(1, MAX_POOL_CT):
        amount = i*10**18
        with brownie.reverts("Only contract owner can call this function."):
            subscriber_contract.create_plan("Test Plan", amount, RATE_LIMIT, RATE_LIMIT, TIME_INTERVAL, _from(bad_guy))
        subscriber_contract.create_plan("Test Plan", amount, RATE_LIMIT, RATE_LIMIT, TIME_INTERVAL, _from(owner))
        subscriber_contract.plan_count() == i

def test_activate_plan(subscriber_contract, accounts):
    owner, bad_guy = accounts[0], accounts[1]
    with brownie.reverts("Plan does not exist."):
        subscriber_contract.activate_plan(0, _from(owner))
    for i in range(1, MAX_POOL_CT):
        amount = i*10**18
        with brownie.reverts("Only contract owner can call this function."):
            subscriber_contract.activate_plan(i, _from(bad_guy))
        with brownie.reverts("Plan does not exist."):
            subscriber_contract.activate_plan(i, _from(owner))
        subscriber_contract.create_plan("Test Plan", amount, RATE_LIMIT, RATE_LIMIT, TIME_INTERVAL, _from(owner))
        subscriber_contract.activate_plan(i, _from(owner))

def test_retire_plan(subscriber_contract, accounts):
    owner, bad_guy = accounts[0], accounts[1]
    for i in range(1, MAX_POOL_CT):
        amount = i*10**18
        with brownie.reverts("Only contract owner can call this function."):
            subscriber_contract.retire_plan(i, _from(bad_guy))
        with brownie.reverts("Plan is not active."):
            subscriber_contract.retire_plan(i, _from(owner))
        subscriber_contract.create_plan("Test Plan", amount, RATE_LIMIT, RATE_LIMIT, TIME_INTERVAL, _from(owner))
        subscriber_contract.activate_plan(i, _from(owner))
        subscriber_contract.retire_plan(i, _from(owner))

def test_retire_contract(subscriber_contract, accounts):
    owner, bad_guy = accounts[0], accounts[1]
    with brownie.reverts("Only contract owner can call this function."):
        subscriber_contract.retire_contract(_from(bad_guy))
    subscriber_contract.retire_contract(_from(owner))
