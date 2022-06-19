from src.analysis.summary_result import SummaryResult

a = SummaryResult(
    "2022-01-01", "2022-05-01", 3, 4, 5
)
b = a.export_as_string()
print(b)