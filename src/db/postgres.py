from typing import Iterable, Optional, Sequence
import psycopg
from psycopg_pool import ConnectionPool

from src.db.dbconfig import DBConfig, DefaultConfig


class Postgres:
    def __init__(self, config: Optional[DBConfig] = None):
        self._config = config if config else DefaultConfig
        self._connection_pool: ConnectionPool = ConnectionPool(
            min_size=1,
            max_size=4,
            kwargs={
                "host": self._config.host,
                "port": self._config.port,
                "dbname": self._config.dbname,
                "user": self._config.user,
                "password": self._config.password,
            },
        )
        print("Connecting to the PostgreSQL database...")

    def query(self, sql, params: Optional[Sequence] = None) -> Iterable:
        with self._connection_pool.connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql, params)
                    return [row for row in cursor]
                except psycopg.errors.ProgrammingError as error:
                    return []

    def store_dataframe(self, df, table):
        # Create a list of tupples from the dataframe values
        rows = [tuple(x) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = ",".join(list(df.columns))
        holders = "%%s," * len(df.columns)
        holders = holders[:-1]
        clause = "INSERT INTO %s(%s) VALUES(" + holders + ") ON CONFLICT DO NOTHING"
        query = clause % (table, cols)
        with self._connection_pool.connection() as connection:
            with connection.cursor() as cursor:

                cursor.executemany(
                    query,
                    rows,
                )

        print(f"store_dataframe() done, {len(rows)} records loaded...")
