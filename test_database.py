import database


def test_get_all_transactions():
    db = database.Database('dog')
    assert db.get_all_transactions()