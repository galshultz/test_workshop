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
            return [
                {'source': t['source'] or None, 'destination': t['destination'],'amount': float(t['amount'])}
                for t in reader
            ]

    def add_transaction(self, source, destination, amount):
        if random() > 0.9:
            raise DatabaseError("DB Conn Fail - err {}".format(uuid4()))

        transactions = self.get_all_transactions()
        transactions.append({'source': source, 'destination': destination,'amount': amount})
        with open(self.file_name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=('source', 'destination', 'amount'))
            writer.writeheader()
            writer.writerows(transactions)

        return True


class DatabaseError(Exception):
    pass