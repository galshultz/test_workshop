import pytest, mock
import transactor
from database import DatabaseError

@pytest.fixture
def mock_db_transaction_source_present():
    return [{'source': 'a',
             'amount': 100.0,
             'destination': 'b'}]

@pytest.fixture
def mock_db_transaction_source_not_present():
    return [{'source': None,
             'amount': 100.0,
             'destination': 'b'}]


def test_transactor_init():
    coin_init = transactor.Transactor('cat')
    assert coin_init

def test_transactor_init_fail():
    with pytest.raises(AssertionError):
        transactor.Transactor('moshe')


def test__calc_address_balance_source_present(mock_db_transaction_source_present):
    with mock.patch('database.Database.get_all_transactions') as mock_database:
        mock_database.return_value = mock_db_transaction_source_present
        transactions = mock_database.return_value
        transactor_test = transactor.Transactor('test')
        assert -100 == transactor_test._calc_address_balance('a',transactions)

def test__calc_address_balance_source_none(mock_db_transaction_source_not_present):
    with mock.patch('database.Database.get_all_transactions') as mock_database:
        mock_database.return_value = mock_db_transaction_source_not_present
        transactions = mock_database.return_value
        transactor_test = transactor.Transactor('test')
        with pytest.raises(AssertionError):
            assert -100 == transactor_test._calc_address_balance('a',transactions)

def test_add_transaction():
    with mock.patch('database.Database.add_transaction') as mock_database:
        mock_database.side_effect = [DatabaseError(), True]
        transactor_test = transactor.Transactor('cat')

        source = 'bea73734-603b-43cf-aa65-ad23d5c3f3e3'
        destination = 'dee4e97f-0a1c-4ec4-8b41-66e9dd5ec9d1'
        amount = 1

        assert transactor_test.add_transaction(source,destination,amount)
