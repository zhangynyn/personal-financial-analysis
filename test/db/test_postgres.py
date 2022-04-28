import unittest

from src.db.postgres import Postgres


class TestPostgres(unittest.TestCase):
    def test_postgres(self):
        pg = Postgres()
        result = pg.query("SELECT 1")
        for row in result:
            print(row)


if __name__ == "__main__":
    unittest.main()
