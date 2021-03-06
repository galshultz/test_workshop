import pytest

@pytest.fixture
def test_transaction_list():
    return [
                {'source': None, 'amount': 100.0, 'destination': 'a'},
                {'source': None, 'amount': 100.0, 'destination': 'b'},
                {'source': 'a', 'amount': 10.0, 'destination': 'b'},
                {'source': 'c', 'amount': 50.0, 'destination': 'd'}
            ]