import pytest, mock
import transactor
from transactor import TransactorGeneralError
from database import DatabaseError


class TestTransactorInit(object):
    def test_transactor_init(self):
        coin_init = transactor.Transactor('cat')
        assert coin_init

    def test_transactor_init_fail(self):
        with pytest.raises(AssertionError):
            transactor.Transactor('moshe')

@mock.patch.object(transactor, 'Database')
class TestPartyBalance(object):

    def test__calc_address_balance_with_existing_source(self, mock_db, test_transaction_list):
        mock_db.get_all_transactions.return_value = test_transaction_list
        transactor_test = transactor.Transactor('')
        assert 90 == transactor_test._calc_address_balance('a',test_transaction_list)

@mock.patch.object(transactor, 'Database')
class TestAddTransactionFails(object):

    def test_add_transaction_one_fail(self,mock_db, test_transaction_list):
        mock_db().get_all_transactions.return_value = test_transaction_list
        mock_db().add_transaction.side_effect = [DatabaseError, None]
        transactor_test = transactor.Transactor('test')

        source = 'a'
        destination = 'b'
        amount = 1

        assert transactor_test.add_transaction(source,destination,amount) == None

    def test_add_transaction_all_fail(self,test_transaction_list):
        with mock.patch('database.Database.add_transaction') as mock_add_transaction:
            with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
                mock_get_all_trnasactions.return_value = test_transaction_list
                mock_add_transaction.side_effect = DatabaseError
                transactor_test = transactor.Transactor('test')

                source = 'a'
                destination = 'b'
                amount = 1

                with pytest.raises(transactor.TransactorGeneralError):
                        transactor_test.add_transaction(source,destination,amount)

    def test_add_transaction_3_retry_attempts(self,mock_db, test_transaction_list):
        # with mock.patch('database.Database.add_transaction') as mock_add_transaction:
        #     with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
        mock_db.get_all_transactions.return_value = test_transaction_list
        mock_db.add_transaction.side_effect = DatabaseError
        transactor_test = transactor.Transactor('test')

        source = 'a'
        destination = 'b'
        amount = 1
        #need to see how can I test the retry attempts
        with pytest.raises(TransactorGeneralError):
            transactor_test.add_transaction(source,destination,amount)


class TestAddTransactionSuccess(object):
    def test_add_transaction_success(self,get_all_transactions):
        with mock.patch('database.Database.add_transaction') as mock_add_transaction:
            with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
                mock_get_all_trnasactions.return_value = get_all_transactions
                transactor_test = transactor.Transactor('test')
                mock_add_transaction.return_value = True

                source = 'a'
                destination = 'b'
                amount = 1

                transactor_test.add_transaction(source, destination, amount)
                mock_add_transaction.assert_called_once_with(source, destination, amount)
