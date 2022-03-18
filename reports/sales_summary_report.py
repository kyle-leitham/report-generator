from enum import Enum
from datetime import date
from pandas import DataFrame
from data.helpers import get_quarter
from data.schema import Columns, TransactionType
from data.transaction import Transaction

REPORT_NAME = 'salesSummaryReport'


class SalesPeriods(Enum):
    INCEPTION_TO_DATE = 'INCEPTION_TO_DATE'
    YEAR_TO_DATE = 'YEAR_TO_DATE'
    QUARTER_TO_DATE = 'QUARTER_TO_DATE'
    MONTH_TO_DATE = 'MONTH_TO_DATE'


class SalesSummaryReport:
    def __init__(self, date_of_report: date):
        self.date_of_report = date_of_report
        self.advisor_sales = DataFrame(
            columns=[
                Columns.ADVISOR.value,
                SalesPeriods.INCEPTION_TO_DATE.value,
                SalesPeriods.YEAR_TO_DATE.value,
                SalesPeriods.QUARTER_TO_DATE.value,
                SalesPeriods.MONTH_TO_DATE.value
            ]
        )

    def process_data(self, transaction: Transaction):
        if transaction.type == TransactionType.SELL.value:
            self.add_sale(
                transaction.advisor,
                transaction.get_total_transaction_amount(),
                transaction.date
            )

    def add_sale(self, advisor: str, total_sale_amount: float, sale_date: date):
        year_to_date = total_sale_amount if sale_date.year == self.date_of_report.year else 0.0
        quarter_to_date = total_sale_amount if get_quarter(sale_date.month) == get_quarter(self.date_of_report.month) else 0.0
        month_to_date = total_sale_amount if sale_date.month == self.date_of_report.month else 0.0

        sale = {
            Columns.ADVISOR.value: advisor,
            SalesPeriods.INCEPTION_TO_DATE.value: total_sale_amount,
            SalesPeriods.YEAR_TO_DATE.value: year_to_date,
            SalesPeriods.QUARTER_TO_DATE.value: quarter_to_date,
            SalesPeriods.MONTH_TO_DATE.value: month_to_date
        }

        self.advisor_sales = self.advisor_sales.append(sale, ignore_index=True)

    def generate(self):
        self.sum_up_sales()
        self.advisor_sales.to_csv(f'{REPORT_NAME}.csv')

    def sum_up_sales(self):
        self.advisor_sales = self.advisor_sales.groupby(Columns.ADVISOR.value).sum().round(2)
