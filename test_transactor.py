import pytest, mock
import transactor
from database import DatabaseError


class TestTransactorInit(object):
    def test_transactor_init(self):
        coin_init = transactor.Transactor('cat')
        assert coin_init

    def test_transactor_init_fail(self):
        with pytest.raises(AssertionError):
            transactor.Transactor('moshe')

class TestPartyBalance(object):
    def test__calc_address_balance_with_existing_source(self, mock_db_transaction_source_present):
        with mock.patch('database.Database.get_all_transactions') as mock_database:
            mock_database.return_value = mock_db_transaction_source_present
            transactions = mock_database.return_value
            transactor_test = transactor.Transactor('test')
            assert -100 == transactor_test._calc_address_balance('a',transactions)

    def test__calc_address_balance_with_no_existing_source(self, mock_db_transaction_source_not_present):
        with mock.patch('database.Database.get_all_transactions') as mock_database:
            mock_database.return_value = mock_db_transaction_source_not_present
            transactions = mock_database.return_value
            transactor_test = transactor.Transactor('test')
            with pytest.raises(AssertionError):
                assert -100 == transactor_test._calc_address_balance('a',transactions)

class TestAddTransactionFails(object):
    def test_add_transaction_one_fail(self,mock_db_get_all_transactions):
        with mock.patch('database.Database.add_transaction') as mock_add_transaction:
            with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
                mock_get_all_trnasactions.return_value = mock_db_get_all_transactions
                mock_add_transaction.side_effect = [DatabaseError, None]
                transactor_test = transactor.Transactor('test')

                source = 'a'
                destination = 'b'
                amount = 1

                assert transactor_test.add_transaction(source,destination,amount) == None

    def test_add_transaction_all_fail(self,mock_db_get_all_transactions):
        with mock.patch('database.Database.add_transaction') as mock_add_transaction:
            with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
                mock_get_all_trnasactions.return_value = mock_db_get_all_transactions
                mock_add_transaction.side_effect = DatabaseError
                transactor_test = transactor.Transactor('test')

                source = 'a'
                destination = 'b'
                amount = 1

                with pytest.raises(transactor.TransactorGeneralError):
                        transactor_test.add_transaction(source,destination,amount)

    def test_add_transaction_all_fail(self,mock_db_get_all_transactions):
        with mock.patch('database.Database.add_transaction') as mock_add_transaction:
            with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
                mock_get_all_trnasactions.return_value = mock_db_get_all_transactions
                mock_add_transaction.side_effect = DatabaseError
                transactor_test = transactor.Transactor('test')

                source = 'a'
                destination = 'b'
                amount = 1

                with pytest.raises(transactor.TransactorGeneralError):
                        transactor_test.add_transaction(source,destination,amount)
                assert mock_add_transaction.call_count == 3

class TestAddTransactionSuccess(object):
    def test_add_transaction_success(self,mock_db_get_all_transactions):
        with mock.patch('database.Database.add_transaction') as mock_add_transaction:
            with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
                mock_get_all_trnasactions.return_value = mock_db_get_all_transactions
                transactor_test = transactor.Transactor('test')
                mock_add_transaction.return_value = True

                source = 'a'
                destination = 'b'
                amount = 1

                transactor_test.add_transaction(source, destination, amount)
                mock_add_transaction.assert_called_once_with(source, destination, amount)
