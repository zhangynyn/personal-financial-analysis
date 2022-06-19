from src.db.postgres import Postgres
from src.db.dbconfig import DBConfig

sqls = [
    """DROP TABLE IF EXISTS credit;""",
    """
    CREATE TABLE credit(
        Uuid VARCHAR(50),
        Institution VARCHAR(10),
        TransDate DATE NOT NULL,
        TransDetails TEXT,
        Debts NUMERIC,
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
    config = DBConfig("mydatabase-instance.czsr2ijvkrza.us-east-1.rds.amazonaws.com", 
                      5432, "postgres", "postgres", "Nangua1208")
    pg = Postgres(config=config)
    for sql in sqls:
        print(sql)
        pg.query(sql)


if __name__ == "__main__":
    replay()
