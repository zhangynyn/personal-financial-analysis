from typing import Iterable, Optional, Sequence

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

    def query(self, sql, params: Optional[Sequence] = None) -> Iterable:
        with self._connection_pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                for row in cursor:
                    yield row
