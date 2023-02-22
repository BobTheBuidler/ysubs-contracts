
import pytest

MAX_POOL_CT = 100
LUSD = "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0"

def _from(account) -> dict:
    return {"from": account}

@pytest.fixture
def subscriber_contract(Subscriber, accounts):
    # deploy the contract with the initial value as a constructor argument
    yield Subscriber.deploy(LUSD, _from(accounts[0]))
