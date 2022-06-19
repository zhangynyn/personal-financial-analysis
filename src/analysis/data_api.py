
from functools import cached_property
from typing import List
from src.analysis.constants import AccountToDataFields, AccountToTable, AccountType
from src.db.postgres import Postgres
import pandas as pd
from datetime import date


class DataAPI:
    @cached_property
    def _pg(self):
        return Postgres()

    def get_transactions_in_dates(self, start_date: date, end_date: date, account_type: AccountType) -> pd.DataFrame:
        table = AccountToTable[account_type]
        sql = f"""
            SELECT * FROM {table}
            WHERE transdate >= %s and transdate < %s;
        """
        result_list = self._pg.query(sql, [start_date, end_date])

        datafields = AccountToDataFields[account_type]
        df = pd.DataFrame(result_list, columns=datafields)

        return df
        