from pandas import DataFrame
from pandas.testing import assert_frame_equal
from datetime import datetime
from data.schema import TransactionType, Columns
from data.transaction import Transaction, TransactionTuple
from reports.sales_summary_report import SalesSummaryReport, SalesPeriods


def test_given_no_sales_then_has_no_sales_records():
    transaction = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            1.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    sales_summary_report = SalesSummaryReport(datetime(2022, 1, 10).date())
    sales_summary_report.process_data(transaction)
    sales_summary_report.sum_up_sales()

    assert len(sales_summary_report.advisor_sales) == 0


def test_given_a_sale_this_month_then_added_to_correct_sales_periods():
    transaction = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    sales_summary_report = SalesSummaryReport(datetime(2022, 1, 10).date())
    sales_summary_report.process_data(transaction)
    sales_summary_report.sum_up_sales()

    expected_df = DataFrame({
        SalesPeriods.INCEPTION_TO_DATE.value: [20.00],
        SalesPeriods.YEAR_TO_DATE.value: [20.00],
        SalesPeriods.QUARTER_TO_DATE.value: [20.00],
        SalesPeriods.MONTH_TO_DATE.value: [20.00]
    }, index=['Advisor'])
    expected_df.index.name = Columns.ADVISOR.value

    assert_frame_equal(sales_summary_report.advisor_sales, expected_df)


def test_given_a_sale_this_quarter_then_added_to_correct_sales_periods():
    transaction = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    sales_summary_report = SalesSummaryReport(datetime(2022, 2, 10).date())
    sales_summary_report.process_data(transaction)
    sales_summary_report.sum_up_sales()

    expected_df = DataFrame({
        SalesPeriods.INCEPTION_TO_DATE.value: [20.00],
        SalesPeriods.YEAR_TO_DATE.value: [20.00],
        SalesPeriods.QUARTER_TO_DATE.value: [20.00],
        SalesPeriods.MONTH_TO_DATE.value: [0.00]
    }, index=['Advisor'])
    expected_df.index.name = Columns.ADVISOR.value

    assert_frame_equal(sales_summary_report.advisor_sales, expected_df)


def test_given_a_sale_this_year_then_added_to_correct_sales_periods():
    transaction = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    sales_summary_report = SalesSummaryReport(datetime(2022, 8, 10).date())
    sales_summary_report.process_data(transaction)
    sales_summary_report.sum_up_sales()

    expected_df = DataFrame({
        SalesPeriods.INCEPTION_TO_DATE.value: [20.00],
        SalesPeriods.YEAR_TO_DATE.value: [20.00],
        SalesPeriods.QUARTER_TO_DATE.value: [0.00],
        SalesPeriods.MONTH_TO_DATE.value: [0.00]
    }, index=['Advisor'])
    expected_df.index.name = Columns.ADVISOR.value

    assert_frame_equal(sales_summary_report.advisor_sales, expected_df)


def test_given_a_sale_previous_year_then_added_to_correct_sales_periods():
    transaction = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    sales_summary_report = SalesSummaryReport(datetime(2023, 8, 10).date())
    sales_summary_report.process_data(transaction)
    sales_summary_report.sum_up_sales()

    expected_df = DataFrame({
        SalesPeriods.INCEPTION_TO_DATE.value: [20.00],
        SalesPeriods.YEAR_TO_DATE.value: [0.00],
        SalesPeriods.QUARTER_TO_DATE.value: [0.00],
        SalesPeriods.MONTH_TO_DATE.value: [0.00]
    }, index=['Advisor'])
    expected_df.index.name = Columns.ADVISOR.value

    assert_frame_equal(sales_summary_report.advisor_sales, expected_df)


def test_given_multiple_sales_then_sales_are_added():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            1.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 3).date(),
            TransactionType.SELL.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    sales_summary_report = SalesSummaryReport(datetime(2022, 8, 10).date())
    sales_summary_report.process_data(transaction1)
    sales_summary_report.process_data(transaction2)
    sales_summary_report.sum_up_sales()

    expected_df = DataFrame({
        SalesPeriods.INCEPTION_TO_DATE.value: [30.00],
        SalesPeriods.YEAR_TO_DATE.value: [30.00],
        SalesPeriods.QUARTER_TO_DATE.value: [0.00],
        SalesPeriods.MONTH_TO_DATE.value: [0.00]
    }, index=['Advisor'])
    expected_df.index.name = Columns.ADVISOR.value

    assert_frame_equal(sales_summary_report.advisor_sales, expected_df)


def test_given_sales_from_two_advisors_then_record_for_each():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor1'
        )
    )

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            10.00,
            1.00,
            'Test Fund',
            'Investor',
            'Advisor2'
        )
    )

    sales_summary_report = SalesSummaryReport(datetime(2023, 8, 10).date())
    sales_summary_report.process_data(transaction1)
    sales_summary_report.process_data(transaction2)
    sales_summary_report.sum_up_sales()

    expected_df = DataFrame({
        SalesPeriods.INCEPTION_TO_DATE.value: [20.00, 10.00],
        SalesPeriods.YEAR_TO_DATE.value: [0.00, 0.00],
        SalesPeriods.QUARTER_TO_DATE.value: [0.00, 0.00],
        SalesPeriods.MONTH_TO_DATE.value: [0.00, 0.00]
    }, index=['Advisor1', 'Advisor2'])
    expected_df.index.name = Columns.ADVISOR.value

    assert_frame_equal(sales_summary_report.advisor_sales, expected_df)