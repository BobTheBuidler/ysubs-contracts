# @version ^0.3.7

from vyper.interfaces import ERC20

CURRENCY: immutable(ERC20)
API_VERSION: immutable(String[8])

struct Plan:
    is_active: bool
    price: uint256

is_active: bool
owner: address
num_plans: uint8
plans: HashMap[uint8, Plan]
subscriptions: HashMap[uint8, HashMap[address, uint256]]

event NewPlan:
    plan_id: uint8
    price: uint256

event NewSubscriber:
    plan_id: uint8
    subscriber: address
    duration: uint256

event Retired:
    ts: uint256

@external
def __init__(currency: address):
    self.owner = msg.sender
    self.is_active = True
    CURRENCY = ERC20(currency)
    API_VERSION = "0.0.0"

##################
# View functions #
##################

@view
@external
def active_plan(subscriber: address) -> (uint8, uint256):
    subscription_end_timestamp: uint256 = 0
    for _i in range(99999):
        i: uint8 = convert(_i, uint8)
        if i > self.num_plans:
            break
        subscription_end_timestamp = self.subscriptions[i][subscriber]
        if subscription_end_timestamp >= block.timestamp:
            return i, subscription_end_timestamp
    return 0, 0

@view
@external
def subscription_end(plan_id: uint8, subscriber: address) -> uint256:
    return self.subscriptions[plan_id][subscriber]

@view
@external
def get_plan(plan_id: uint8) -> Plan:
    return self.plans[plan_id]

@view
@external
def plan_count() -> uint8:
    return self.num_plans

########################
# Subscriber functions #
########################

@external
def subscribe(plan_id: uint8, amount: uint256) -> uint256:
    return self._subscribe(plan_id, amount, msg.sender)

@external
def subscribe_for(plan_id: uint8, amount: uint256, wallet: address) -> uint256:
    return self._subscribe(plan_id, amount, wallet)

######################
# Internal functions #
######################

@internal
def _subscribe(plan_id: uint8, amount: uint256, subscriber: address) -> uint256:
    assert self.is_active, "Subscription contract has been retired"
    plan: Plan = self.plans[plan_id]
    assert plan.is_active, "Plan does not exist or has been retired."
    CURRENCY.transferFrom(subscriber, self, amount)
    duration: uint256 = amount / plan.price
    log NewSubscriber(plan_id, subscriber, duration)
    end_timestamp: uint256 = block.timestamp + duration
    self.subscriptions[plan_id][subscriber] = end_timestamp
    return end_timestamp

###################
# Owner functions #
###################

@external
def create_plan(price: uint256) -> Plan:
    assert self.is_active, "Subscription contract has been retired"
    assert self.owner == msg.sender, "You are not the owner."
    plan: Plan = Plan({is_active: False, price: price})
    plan_id: uint8 = self.num_plans + 1
    self.plans[plan_id] = plan
    self.num_plans = plan_id
    log NewPlan(plan_id, price)
    return plan

@external
def activate_plan(plan_id: uint8):
    assert self.is_active, "Subscription contract has been retired"
    assert self.owner == msg.sender, "You are not the owner."
    plan: Plan = self.plans[plan_id]
    assert plan.price > 0, "Plan does not exist."
    assert not plan.is_active, "Plan is already active."
    self.plans[plan_id].is_active = True

@external
def retire_plan(plan_id: uint8):
    assert self.is_active, "Subscription contract has been retired"
    assert self.owner == msg.sender, "You are not the owner."
    plan: Plan = self.plans[plan_id]
    assert plan.is_active, "Plan is not active."
    plan.is_active = False

@external
def retire_contract():
    assert self.is_active, "Subscription contract has been retired"
    assert self.owner == msg.sender, "You are not the owner."
    self.is_active = False
    log Retired(block.timestamp)
