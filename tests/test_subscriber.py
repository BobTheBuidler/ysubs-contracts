import brownie

from fixtures import _from, subscriber_contract

def test_create_plan(subscriber_contract, accounts):
    owner, bad_guy = accounts[0], accounts[1]
    with brownie.reverts("You are not the owner."):
        subscriber_contract.create_plan(10**18, _from(bad_guy))
    subscriber_contract.create_plan(10**18, _from(owner))

def test_activate_plan(subscriber_contract, accounts):
    owner, bad_guy = accounts[0], accounts[1]
    with brownie.reverts("You are not the owner."):
        subscriber_contract.activate_plan(1, _from(bad_guy))
    with brownie.reverts("Plan does not yet exist."):
        subscriber_contract.activate_plan(1, _from(owner))
    subscriber_contract.create_plan(10**18, _from(owner))
    subscriber_contract.activate_plan(1, _from(owner))

def test_retire_plan(subscriber_contract, accounts):
    owner, bad_guy = accounts[0], accounts[1]
    with brownie.reverts("You are not the owner."):
        subscriber_contract.retire_plan(1, _from(bad_guy))
    with brownie.reverts("Plan is not active."):
        subscriber_contract.retire_plan(1, _from(owner))
    subscriber_contract.create_plan(10**18, _from(owner))
    subscriber_contract.activate_plan(1, _from(owner))
    subscriber_contract.retire_plan(1, _from(owner))
