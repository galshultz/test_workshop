import database
import transactor
from transactor import Coin

transactor = transactor.Transactor(Coin.CAT)
db = database.Database('test')
transactions = db.get_all_transactions()
for i in transactions:
    print i