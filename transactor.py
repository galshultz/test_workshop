from database import Database, DatabaseError
import logging
import sys

# setup logging configuration
logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG,
    format='[%(asctime)s][%(name)s][%(levelname)s][%(funcName)s]:%(message)s'
)


class Coin(object):
    """Supported Coin Types"""
    CAT = 'cat'
    DOG = 'dog'


class Transactor(object):
    """Manage transaction validation and book keeping of coins"""
    _ADD_RETRY_ATTEMPTS = 2

    def __init__(self, coin_type):
        """instantiate a new Transactor instance for a specific coin type"""

        self.coin_type = coin_type
        self.db = Database(coin_type)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting a new instance for coin '{}'".format(self.coin_type))

    def add_transaction(self, source, destination, amount):
        """
        Validate and persist a transaction between source and destination addresses
        :param source: the giving party
        :type source: unicode
        :param destination: the receiving party
        :type destination: unicode
        :param amount: amount of coins for the transaction
        :type amount: int or float
        """
        amount = float(amount)
        self._validate_transaction(source, destination, amount)
        self._add_transaction(source, destination, amount)

    @staticmethod
    def _calc_address_balance(address, transactions):
        in_amount = sum(t['amount'] for t in transactions if t['destination'] == address) or 0.0
        out_amount = sum(t['amount'] for t in transactions if t['source'] == address) or 0.0
        return in_amount - out_amount

    def _validate_transaction(self, source, destination, amount):
        if not self._not_self_transaction(source, destination):
            raise InvalidTransaction("does not support self transactions")

        if not self._source_credit_is_valid(source, amount):
            raise InvalidTransaction(
                "source '{}' credit cannot support the required transaction".format(source.encode('utf-8'))
            )

    def _not_self_transaction(self, source, destination):
        return source != destination

    def _source_credit_is_valid(self, source_address, amount):
        """Validates that the source address has the necessary funds to perform the required transaction"""

        transactions = self.db.get_all_transactions()
        balance = self._calc_address_balance(source_address, transactions)
        self.logger.debug("Source {} balance: {}{}s".format(source_address.encode('utf-8'), balance, self.coin_type))

        return amount <= balance

    def _add_transaction(self, source, destination, amount, retry_attempts=_ADD_RETRY_ATTEMPTS):
        """persists a valid transaction in the database"""

        try:
            self.db.add_transaction(source, destination, amount)

        except DatabaseError:
            if retry_attempts > 0:
                self.logger.warning("Failed to save transaction to DB - Retrying", exc_info=True)
                return self._add_transaction(source, destination, amount, retry_attempts=retry_attempts-1)

            self.logger.exception("Failed to save transaction to database - Retry attempts exceeded")
            raise TransactorGeneralError("Failed to save transaction to DB")

        else:
            self.logger.info("Successfully added transaction")


class TransactorGeneralError(Exception):
    pass


class InvalidTransaction(TransactorGeneralError):
    pass
