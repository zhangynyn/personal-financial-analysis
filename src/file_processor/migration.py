from src.db.postgres import Postgres

sqls = [
    """DROP TABLE IF EXISTS cibc_credit;""",
    """
    CREATE TABLE credit(
        Uuid VARCHAR(50),
        Institution VARCHAR(10),
        TransDate DATE NOT NULL,
        TransDetails TEXT,
        Debits NUMERIC,
        Credits NUMERIC,
        CardNumber VARCHAR(20),
        PRIMARY KEY(Institution,TransDate,TransDetails)
    );
    """,
    """DROP TABLE IF EXISTS chequing;""",
    """
    CREATE TABLE chequing(
        Uuid VARCHAR(50),
        Institution VARCHAR(10),
        TransDate DATE NOT NULL,
        TransDetails TEXT,
        Withdrawals NUMERIC,
        Deposits NUMERIC,
        PRIMARY KEY(Institution,TransDate,TransDetails)
    );
    """,
]


def replay():
    print("Migrating database...")
    pg = Postgres()
    for sql in sqls:
        print(sql)
        pg.query(sql)


if __name__ == "__main__":
    replay()
