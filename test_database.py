import csv
import database
import transactor

class TestIntegration(object):

    def force_add_transaction(self, db, source, destination, amount):
        file_name = 'database/coins/test.csv'
        transactions = db.get_all_transactions()
        transactions.append({'source': source, 'destination': destination,'amount': amount})
        transactions = db._prep_transactions_to_db(transactions)
        with open(file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=('source', 'destination', 'amount'))
            writer.writeheader()
            writer.writerows(transactions)

    def test_get_all_transactions(self):
        db = database.Database('dog')
        assert db.get_all_transactions()

    def test_add_transaction(self):
        db = database.Database('test')
        source = 'a'
        destination = 'b'
        amount = 1
        assert db.add_transaction(source,destination, amount) == True

    def test_add_transaction_sucess(self):
        test_transactor = transactor.Transactor('test')
        db = database.Database('test')
        self.force_add_transaction(db, 'a', 'b', 50)
        test_transactor.add_transaction('b','a', 10)
