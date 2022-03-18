from pandas import DataFrame
from pandas.testing import assert_frame_equal
from datetime import datetime
from data.schema import TransactionType, Columns
from data.transaction import Transaction, TransactionTuple
from reports.assets_under_management_summary_report import AssetsUnderManagementSummaryReport, ASSET_UNDER_MANAGEMENT


def test_given_two_buys_then_assets_are_added():
    transaction1 = Transaction(
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

    transaction2 = Transaction(
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

    assets_under_management_summary_report = AssetsUnderManagementSummaryReport()
    assets_under_management_summary_report.process_data(transaction1)
    assets_under_management_summary_report.process_data(transaction2)
    assets_under_management_summary_report.calculate_assets_under_management()

    expected_df = DataFrame({
        Columns.ADVISOR.value: ['Advisor'],
        ASSET_UNDER_MANAGEMENT: [40.00]
    })

    assert_frame_equal(assets_under_management_summary_report.assets_under_management, expected_df)


def test_given_buy_and_sell_then_sold_assets_are_subtracted():
    transaction1 = Transaction(
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

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.SELL.value,
            5.00,
            2.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    assets_under_management_summary_report = AssetsUnderManagementSummaryReport()
    assets_under_management_summary_report.process_data(transaction1)
    assets_under_management_summary_report.process_data(transaction2)
    assets_under_management_summary_report.calculate_assets_under_management()

    expected_df = DataFrame({
        Columns.ADVISOR.value: ['Advisor'],
        ASSET_UNDER_MANAGEMENT: [10.00]
    })

    assert_frame_equal(assets_under_management_summary_report.assets_under_management, expected_df)


def test_given_asset_price_changes_then_held_shares_updated():
    transaction1 = Transaction(
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

    transaction2 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
            5.00,
            4.00,
            'Test Fund',
            'Investor',
            'Advisor'
        )
    )

    assets_under_management_summary_report = AssetsUnderManagementSummaryReport()
    assets_under_management_summary_report.process_data(transaction1)
    assets_under_management_summary_report.process_data(transaction2)
    assets_under_management_summary_report.calculate_assets_under_management()

    expected_df = DataFrame({
        Columns.ADVISOR.value: ['Advisor'],
        ASSET_UNDER_MANAGEMENT: [60.00]
    })

    assert_frame_equal(assets_under_management_summary_report.assets_under_management, expected_df)


def test_given_transactions_for_two_advisors_then_record_for_each():
    transaction1 = Transaction(
        TransactionTuple(
            datetime(2022, 1, 2).date(),
            TransactionType.BUY.value,
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
            TransactionType.BUY.value,
            5.00,
            4.00,
            'Test Fund',
            'Investor',
            'Advisor2'
        )
    )

    assets_under_management_summary_report = AssetsUnderManagementSummaryReport()
    assets_under_management_summary_report.process_data(transaction1)
    assets_under_management_summary_report.process_data(transaction2)
    assets_under_management_summary_report.calculate_assets_under_management()

    expected_df = DataFrame({
        Columns.ADVISOR.value: ['Advisor1', 'Advisor2'],
        ASSET_UNDER_MANAGEMENT: [40.00, 20.00]
    })

    assert_frame_equal(assets_under_management_summary_report.assets_under_management, expected_df)
