from dataclasses import dataclass


@dataclass
class SummaryResult:
    StartDate: str
    EndDate: str
    TotalSpend: float
    TotalIncome: float
    CurrentMonthBalance: float

    def export_as_string(self):
        report = {}
        report["TotalSpend"] = f'Total Spend from {self.StartDate} to {self.EndDate} is: {self.TotalSpend}'
        report["TotalIncome"] = f'Total Income from {self.StartDate} to {self.EndDate} is: {self.TotalIncome}'
        report["CurrentMonthBalance"] = f'Monthly Balance from {self.StartDate} to {self.EndDate} is: {self.CurrentMonthBalance}'
        return report

    #def export_as_txt_file(self):
        #pdf_printer( f"{self.StartDate} to {self.EndDate} the spending ")

    #def export_as_image(self):
        #image_printer( f"{self.StartDate} to {self.EndDate} the spending ")
