from pandas import DataFrame
from pandas.testing import assert_frame_equal
from datetime import datetime
from data.schema import TransactionType, Columns
from data.transaction import Transaction, TransactionTuple
from reports.break_report import BreakReport, ERROR, NEGATIVE_CASH_BALANCE, NEGATIVE_SHARE_BALANCE_FOR


def test_given_investor_buys_more_than_sells_then_report_negative_cash_balance():
    transaction = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            10.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    break_report = BreakReport()
    break_report.process_data(transaction)
    break_report.find_erroneous_balances()

    expected_df = DataFrame({
        Columns.INVESTOR.value: ['Investor'],
        ERROR: [NEGATIVE_CASH_BALANCE]
    })

    assert_frame_equal(break_report.errors, expected_df)


def test_given_investor_sells_more_shares_than_holds_then_report_negative_share_balance():
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

    break_report = BreakReport()
    break_report.process_data(transaction)
    break_report.find_erroneous_balances()

    expected_df = DataFrame({
        Columns.INVESTOR.value: ['Investor'],
        ERROR: [f'{NEGATIVE_SHARE_BALANCE_FOR} Test Fund']
    })

    assert_frame_equal(break_report.errors, expected_df)