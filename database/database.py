import os.path
import csv
from random import random
from uuid import uuid4

class Database(object):
    def __init__(self, coin):
        self.file_name = 'database/coins/{}.csv'.format(coin)
        assert os.path.isfile(self.file_name), "Unknown Coin"

    def get_all_transactions(self):
        with open(self.file_name) as f:
            reader = csv.DictReader(f)
            return [{
                'source': t['source'].decode('utf-8') or None,
                'destination': t['destination'].decode('utf-8'),
                'amount': float(t['amount'])
            } for t in reader]

    def add_transaction(self, source, destination, amount):
        if random() > 0.01:
            raise DatabaseError("DB Conn Fail - err {}".format(uuid4()))

        transactions = self.get_all_transactions()
        transactions.append({'source': source, 'destination': destination,'amount': amount})
        transactions = self._prep_transactions_to_db(transactions)
        with open(self.file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=('source', 'destination', 'amount'))
            writer.writeheader()
            writer.writerows(transactions)

        return True

    @staticmethod
    def _prep_transactions_to_db(transactions):
        return [{
            'source': t['source'].encode('utf-8') if t['source'] else None,
            'destination': t['destination'].encode('utf-8'),
            'amount': t['amount']
        } for t in transactions]

    def __del__(self):
        if self.file_name == 'database/coins/test.csv':
            print "purge test db"
            with open(self.file_name, 'w') as f:
                f.write('source,destination,amount\n')


class DatabaseError(Exception):
    pass