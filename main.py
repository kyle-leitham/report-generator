import sys
from pandas import DataFrame, read_csv
from datetime import date
from cost_basis.cost_basis_calculator_factory import CostBasisMethod, CostBasisCalculatorFactory
from data.schema import validate, Columns
from data.helpers import clean_data
from data.transaction import Transaction
from reports.sales_summary_report import SalesSummaryReport
from reports.assets_under_management_summary_report import AssetsUnderManagementSummaryReport
from reports.break_report import BreakReport
from reports.investor_profit_report import InvestorProfitReport


def main():
    data_frame = try_read_csv_to_data_frame()
    if data_frame is None:
        return

    cost_basis_method = try_get_cost_basis_method()
    if cost_basis_method is None:
        return

    data_frame = clean_data(data_frame)

    if data_is_valid(data_frame):
        generate_reports(data_frame, cost_basis_method, date.today())


def try_read_csv_to_data_frame() -> DataFrame:
    data_frame = None

    try:
        csv_file_name = sys.argv[1]
        data_frame = read_csv(csv_file_name)
    except IndexError:
        print('No file name given')
    except FileNotFoundError:
        print(f'File {csv_file_name} does not exist')

    return data_frame


def try_get_cost_basis_method():
    try:
        cost_basis_method = sys.argv[2]
        CostBasisCalculatorFactory().create_cost_basis_calculator(cost_basis_method.upper())
    except IndexError:
        return CostBasisMethod.AVERAGE_COST.value  # Default
    except NotImplementedError:
        print('Selected cost basis method has not been implemented yet')
        return None
    except ValueError:
        print('Invalid cost basis method')
        return None


def data_is_valid(data_frame: DataFrame) -> bool:
    validation_errors = validate(data_frame)

    if len(validation_errors) > 0:
        for validation_error in validation_errors:
            print(validation_error.__str__())
        return False

    return True


def generate_reports(data_frame: DataFrame, cost_basis_method: CostBasisMethod, date_of_report: date):
    reports = [
        SalesSummaryReport(date_of_report),
        AssetsUnderManagementSummaryReport(),
        BreakReport(),
        InvestorProfitReport(cost_basis_method, CostBasisCalculatorFactory())
    ]

    data_frame = data_frame.sort_values(by=Columns.TXN_DATE.value)

    for transaction_data in data_frame.itertuples():
        for report in reports:
            transaction = Transaction(transaction_data)
            report.process_data(transaction)

    for report in reports:
        report.generate()


if __name__ == '__main__':
    main()
