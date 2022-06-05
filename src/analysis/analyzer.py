import pandas as pd
from src.analysis.data_api import DataAPI
from src.analysis.summary_result_api import SummaryResultAPI
from src.analysis.constants import AccountType, InstitutionMap
import datetime

class Analyzer:
    def __init__(self, data_api: DataAPI) -> None:
        self._data_api = data_api
    
    def get_summary_result(self, start_date, end_date, account_type:AccountType, institution = None):
        transaction_data = self._data_api.get_transactions_in_dates(datetime.datetime.strptime(start_date, "%Y-%m-%d"),
                                                                    datetime.datetime.strptime(end_date, "%Y-%m-%d"), 
                                                                    account_type)
        
        if institution is not None:
            transaction_data = transaction_data[transaction_data["Institution"] == InstitutionMap[institution]]

        summary_result_api = SummaryResultAPI()
        summary_result_api.StartDate = start_date
        summary_result_api.EndDate = end_date

        if account_type == AccountType.CHEQUING:
            summary_result_api.TotalSpend = transaction_data["Withdrawals"].sum()
            summary_result_api.TotalIncome = transaction_data["Deposits"].sum()
            summary_result_api.CurrentMonthBalance = -summary_result_api.TotalSpend + summary_result_api.TotalIncome
        
        if account_type == AccountType.CREDIT:
            summary_result_api.TotalSpend = transaction_data["Debts"].sum()
            summary_result_api.TotalIncome = transaction_data["Credits"].sum()
            summary_result_api.CurrentMonthBalance = -summary_result_api.TotalSpend + summary_result_api.TotalIncome
        
        return summary_result_api
        