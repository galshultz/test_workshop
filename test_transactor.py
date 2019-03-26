import pytest, mock
import transactor
from transactor import TransactorGeneralError, InvalidTransaction
from database import DatabaseError
import csv


class TestTransactorInit(object):
    def test_transactor_init(self):
        coin_init = transactor.Transactor('cat')
        assert coin_init

    def test_transactor_init_fail(self):
        with pytest.raises(AssertionError):
            transactor.Transactor('moshe')


@mock.patch.object(transactor, 'Database')
class TestAddTransactionFails(object):

    def test_add_transaction_source_does_not_have_sufficient_funds(self, mock_db, test_transaction_list):
        mock_db().get_all_transactions.return_value = test_transaction_list
        transactor_test = transactor.Transactor('test')
        source = 'a'
        destination = 'b'
        amount = 100
        with pytest.raises(InvalidTransaction):
            assert transactor_test.add_transaction(source, destination, amount)

    def test_add_transaction_source_does_not_exists(self, mock_db, test_transaction_list):
        mock_db().get_all_transactions.return_value = test_transaction_list
        transactor_test = transactor.Transactor('test')
        source = 'moshe'
        destination = 'b'
        amount = 100
        with pytest.raises(InvalidTransaction):
            assert transactor_test.add_transaction(source, destination, amount)


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

                with pytest.raises(TransactorGeneralError):
                        transactor_test.add_transaction(source,destination,amount)

    def test_add_transaction_3_retry_attempts(self,mock_db, test_transaction_list):
        # with mock.patch('database.Database.add_transaction') as mock_add_transaction:
        #     with mock.patch('database.Database.get_all_transactions') as mock_get_all_trnasactions:
        mock_db().get_all_transactions.return_value = test_transaction_list
        mock_db().add_transaction.side_effect = DatabaseError
        transactor_test = transactor.Transactor('test')

        source = 'a'
        destination = 'b'
        amount = 1
        #need to see how can I test the retry attempts
        transactor_test.add_transaction(source, destination, amount)
        assert mock_db.add_transaction.call_count == 3


@mock.patch.object(transactor, 'Database')
class TestUnitAddTransactionSuccess(object):
    def test_unit_add_transaction_success(self,mock_db, test_transaction_list):
        with mock.patch('transactor.Transactor.add_transaction') as mock_add_transaction:
            mock_db().get_all_transactions.return_value = test_transaction_list
            mock_db().add_transaction.return_value = True
            transactor_test = transactor.Transactor('test')

            source = 'a'
            destination = 'b'
            amount = 1

            transactor_test.add_transaction(source, destination, amount)
            mock_add_transaction.assert_called_once_with(source, destination, amount)


class TestIntegrationAddTransactionSuccess(object):


    def force_add_transaction(self, db, source, destination, amount):
        file_name = 'database/coins/test.csv'
        transactions = db.get_all_transactions()
        transactions.append({'source': source, 'destination': destination,'amount': amount})
        transactions = db._prep_transactions_to_db(transactions)
        with open(file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=('source', 'destination', 'amount'))
            writer.writeheader()
            writer.writerows(transactions)

    def test_integration_add_transaction_success(self):
            transactor_test = transactor.Transactor('test')
            self.force_add_transaction(transactor_test.db, None, 'a', 10)
            source = 'a'
            destination = 'b'
            amount = 1

            assert transactor_test.add_transaction(source, destination, amount) == None
