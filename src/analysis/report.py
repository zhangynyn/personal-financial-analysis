from src.analysis.data_api import DataAPI
from src.analysis.analyzer import Analyzer
from src.analysis.summary_result_api import SummaryResultAPI
from src.analysis.constants import AccountType, Institution


class Report:
    def __init__(self, summary_result_api: SummaryResultAPI) -> None:
        self._summary_result_api = summary_result_api
    
    def generate_summary_report(self):
        print("Generating Report...")
        print("----------------------------------------------")
        print(f'Total Spend from {self._summary_result_api.StartDate} to {self._summary_result_api.EndDate} is: {self._summary_result_api.TotalSpend}')
        print(f'Total Income from {self._summary_result_api.StartDate} to {self._summary_result_api.EndDate} is: {self._summary_result_api.TotalIncome}')
        print(f'Monthly Balance from {self._summary_result_api.StartDate} to {self._summary_result_api.EndDate} is: {self._summary_result_api.CurrentMonthBalance}')


api = DataAPI()
analyzer = Analyzer(data_api=api)

# Test generate  report
# Case 1
chequing_result = analyzer.get_summary_result("2022-03-01", "2022-04-01", AccountType.CHEQUING)
Report(chequing_result).generate_summary_report()

# Case 2
cibc_chequing_result = analyzer.get_summary_result("2022-03-01", "2022-04-01", AccountType.CHEQUING, Institution.CIBC)
Report(cibc_chequing_result).generate_summary_report()

# Case 3
scotia_chequing_result = analyzer.get_summary_result("2022-03-01", "2022-04-01", AccountType.CHEQUING, Institution.SCOTIABANK)
Report(scotia_chequing_result).generate_summary_report()

# Case 4
cibc_credit_result = analyzer.get_summary_result("2022-03-01", "2022-04-01", AccountType.CREDIT, Institution.CIBC)
Report(cibc_credit_result).generate_summary_report()
